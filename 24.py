import Image

def GetNeighbors(d):
    x, y = d[0], d[1]
    return [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]

def IsInsideMaze(maze, p):
    w, h = maze.size
    x, y = p[0], p[1]
    return ((0 <= p[0] < w) and (0 <= p[1] < h))

def MazeBFS(maze, graph, start, end):
    WALL = (255, 255, 255)
    VISITED = (0, 0, 255)
    maze.putpixel(start, VISITED)
    maze.putpixel(end, VISITED)
    queue = [end]
    while queue:
        d = queue.pop(0)
        for neighbor in GetNeighbors(d):
            if IsInsideMaze(maze, neighbor):                
                if maze.getpixel(neighbor) != VISITED and maze.getpixel(neighbor) != WALL:
                    graph[neighbor] = d
                    maze.putpixel(neighbor, VISITED)
                    queue.append(neighbor)

maze = Image.open('maze.png').convert('RGB')
graph = {}
w, h = maze.size
entrance = (w-2, 0)
exit = (1, h-1)
MazeBFS(maze, graph, entrance, exit)

maze = Image.open('maze.png').convert('RGB')
top = (w-2, 1)
buttom = (1, h-2)
zip_bytes = []
i = 0
# from top to bottom
pixel_location = top
while pixel_location != buttom:
    if i % 2 == 0:
        zip_bytes.append(maze.getpixel(pixel_location)[0])
    pixel_location = graph[pixel_location]
    i = i + 1

open('maze.zip','wb').write(bytearray(zip_bytes))

print "Done creating Zip Level: 24!"
