import pygame
import random
import math
import copy
from pygame import Rect, Surface
from typing import TypeVar

A = TypeVar('A')

# class Agent:
#     def __init__(self, rect: Rect, color):
#         self.rect = rect
#         self.hidden = False
#         self.color = color

#     def update(self) -> None:
#         return
    
#     def draw(self, surface: Surface) -> None:
#         surface.fill(self.color)

class Environment:
    def __init__(self, screenRect):
        self.agents = []
        self.screenRect = screenRect
        self.surfaces = dict()
        self.counter = 0


    def spreadAgentsRandomly(self):
        """
        Distributes agents randomly over the environment As a result, some agents
        might overlap. If you want to be absolutely sure that agents do not share a
        part of their available space, spread them out evenly. 
        """
        screenWidth = self.screenRect.width
        screenHeight = self.screenRect.height
        for agent in self.agents:
            agent.rect.x = random.randint(0, screenWidth - agent.rect.width)
            agent.rect.y = random.randint(0, screenHeight - agent.rect.height)


    def spreadAgentsEvenly(self):
        """
        Distributes agents evenly over the available space. 
        Assumes that all agents are of equal width and height. 

        If this is not the case, make sure the agent in 
        `Environment.agents[0]` is of representative size. 
        """
        if len(self.agents) == 0:
            return
        agentRect = self.agents[0].rect
        screenRect = self.screenRect
        ratioAgent = agentRect.width / agentRect.height
        ratioScreen = screenRect.width / screenRect.height
        rowColumnRatio = ratioScreen / ratioAgent

        # Ratio = width / height, so r > 1 means wide, r < 1 means long
        # Dividing ratios yields column/row separation

        # Example: say agents are wide but screen is long.  
        # Then ratioAgent = 2 and ratioScreen = 0.5
        # Then rowColumnRatio = 0.5/2 = 0.25. This means #columns = #rows * 0.25
        # Additionally, we have that #columns * #rows >= #agents
        # Then #columns = #agents / #rows
        # Substituting, this yields 
        # #agents/#rows = #rows * ratio 
        # #agents = #rows^2 * ratio
        # #rows = sqrt(#agents / ratio)
        numRows = math.ceil(math.sqrt(len(self.agents) / rowColumnRatio))
        numColumns = math.ceil(len(self.agents) / numRows)
        cellWidth = screenRect.width / numColumns
        cellHeight = screenRect.height / numRows

        currentX = 0
        currentY = 0
        agentsShuffled = self.agents.copy()
        random.shuffle(agentsShuffled)
        rowCounter = 0
        for agent in agentsShuffled:
            cellRect = Rect(currentX, currentY, cellWidth, cellHeight)
            agent.rect.center = cellRect.center
            currentX += cellWidth
            rowCounter += 1
            if rowCounter >= numColumns:
                currentX = 0
                currentY += cellHeight
                rowCounter = 0


    def findFreeSpace(self, agent, maxRadius: int = None) -> Rect:
        """
        Finds a random free space in the environment where the given agent might
        fit. Use the radius to force the new spot to be within the given distance of
        the old spot. 

        Returns a new Rect which can be used as location for the agent. Might return
        None if no new spot was found. 
        """
        # Rather dumb approach: try random coords and hope they work
        agentRects = list(map(lambda a : a.rect, self.agents))
        for i in range(0, 10000):
            if maxRadius is not None:
                deltaX = random.randint(-maxRadius, maxRadius)
                newX = agent.rect.x + deltaX
                newX = max(0, min(self.screenRect.width - agent.rect.width, newX))
                newY = agent.rect.y + (maxRadius - abs(deltaX)) * random.choice([1, -1])
                newY = max(0, min(self.screenRect.height - agent.rect.height, newY))
            else:
                newX = random.randint(0, self.screenRect.width - agent.rect.width)
                newY = random.randint(0, self.screenRect.height - agent.rect.height)
            newRect = Rect(newX, newY, agent.rect.width, agent.rect.height)
            collision = newRect.collidelist(agentRects)
            if collision == -1:
                # No collision found
                return newRect
        return None
    

    def findCloseNeighbours(self, agent, radius: int, filterFun = None) -> list:
        """
        Finds agents around the given agent within the given radius. Use the
        filterFun to constrain the search to agents satisfying the given criteria.
        If no filterFun is provided, only the radius will be used to limit the
        search results. 

        Returns a list of agents. The list might be empty if no close neighbours
        were found. 
        """
        findRect = Rect(0, 0, radius + agent.rect.width, radius + agent.rect.height)
        findRect.center = agent.rect.center
        agents = self.agents
        if filterFun is not None:
            agents = filter(filterFun, agents)
        
        close = [a for a in agents if findRect.colliderect(a.rect)]
        return close
    
    def findAgents(self, filterFun = None) -> list:
        """
        Returns a list of agents satisfying the given criteria. Use the optional
        filterFun to force agents to satisfy your criteria. 

        Returns a list of agents. If filterFun is None, all agents in the
        environment will be returned. 
        """
        if filterFun is None:
            return self.agents.copy()
        return list(filter(filterFun, self.agents))


    def addAgent(self, agent):
        """
        Registers an agent with this environment. The given agent should at least
        have a "rect" and "hidden" property, and the functions "update" and "draw". 

        After registering, this environment will be responsible for calling these
        functions at the appropriate times. 
        """
        self.agents.append(agent)
        surface = Surface((agent.rect.width, agent.rect.height))
        self.surfaces[agent] = surface


    def removeAgent(self, agent):
        """
        De-registers the given agent from this environment. 
        """
        self.surfaces.pop(agent)
        self.agents.remove(agent)


    def draw(self, screen: Surface):
        """
        Draws this environment, including all agents, to the given surface. 
        """
        for (agent, surface) in self.surfaces.items():
            if not agent.hidden:
                agent.draw(surface)
                screen.blit(surface, agent.rect)


    def update(self, useDeepCopy = True):
        """
        Updates the board to the next "tick". Updates all agents by calling their
        "update" functions. 

        Makes copies of the old state of the agents to allow all agent updates to be
        applied atomically. If this copy-behavior is undesirable, switch it off
        using the flag. 
        """
        self.counter += 1

        i = 0
        newAgents = []
        while i < len(self.agents):
            if useDeepCopy:
                existing = self.agents[i]
                copied = copy.deepcopy(existing)
                existing.update(self)
                newAgents.append(existing)
                self.agents[i] = copied
            else:
                self.agents[i].update(self)

            i += 1

        if useDeepCopy:
            self.agents = newAgents

