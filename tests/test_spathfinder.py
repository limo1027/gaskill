import unittest

from gaskill.spathfinder import astar, dijkstra, bfs, bidirectional_bfs, dfs_maker, astar_cost, dijkstra_cost, get_path_cost, create_cost_grid


class TestPathfinding(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]

    def test_astar(self):
        path = astar(self.grid, (0, 0), (4, 4))
        self.assertIsNotNone(path)
        self.assertTrue(len(path) > 0)

    def test_astar_blocked(self):
        grid = [
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]
        path = astar(grid, (0, 0), (2, 2))
        self.assertIsNone(path)

    def test_dijkstra(self):
        path = dijkstra(self.grid, (0, 0), (4, 4))
        self.assertIsNotNone(path)

    def test_bfs(self):
        path = bfs(self.grid, (0, 0), (4, 4))
        self.assertIsNotNone(path)

    def test_bidirectional_bfs(self):
        path = bidirectional_bfs(self.grid, (0, 0), (4, 4))
        self.assertIsNotNone(path)

    def test_astar_diagonal(self):
        path = astar(self.grid, (0, 0), (4, 4), allow_diagonal=True)
        self.assertIsNotNone(path)
        self.assertTrue(len(path) > 0)


class TestMazeGeneration(unittest.TestCase):
    def test_dfs_maker(self):
        maze = dfs_maker(11, 11, seed=42)
        self.assertEqual(len(maze), 11)
        self.assertEqual(len(maze[0]), 11)

    def test_maze_has_path(self):
        maze = dfs_maker(9, 9, seed=42)
        path = bfs(maze, (1, 1), (7, 7))
        self.assertIsNotNone(path)


class TestCostPathfinding(unittest.TestCase):
    def setUp(self):
        # 创建一个成本网格：-1=障碍，0=无成本，1=普通路，5=泥地，10=沼泽
        self.cost_grid = [
            [1, 1, 1, 1, 1],
            [1, -1, -1, -1, 1],
            [1, 5, 5, 5, 1],
            [1, -1, -1, -1, 1],
            [1, 1, 1, 1, 1]
        ]

    def test_astar_cost_basic(self):
        path = astar_cost(self.cost_grid, (0, 0), (4, 4))
        self.assertIsNotNone(path)
        self.assertTrue(len(path) > 0)

    def test_astar_cost_avoid_high_cost(self):
        path = astar_cost(self.cost_grid, (0, 0), (4, 0))
        self.assertIsNotNone(path)
        # 路径应该避开泥地（成本5），走上面的路
        for point in path:
            x, y = int(point.x), int(point.y)
            self.assertNotEqual(self.cost_grid[y][x], 5)

    def test_dijkstra_cost_basic(self):
        path = dijkstra_cost(self.cost_grid, (0, 0), (4, 4))
        self.assertIsNotNone(path)
        self.assertTrue(len(path) > 0)

    def test_astar_cost_blocked(self):
        cost_grid = [
            [1, 1, -1],
            [-1, 1, -1],
            [1, -1, 1]
        ]
        path = astar_cost(cost_grid, (0, 0), (2, 2))
        self.assertIsNone(path)

    def test_astar_cost_diagonal(self):
        path = astar_cost(self.cost_grid, (0, 0), (4, 4), allow_diagonal=True)
        self.assertIsNotNone(path)

    def test_astar_cost_zero_cost(self):
        cost_grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        path = astar_cost(cost_grid, (0, 0), (2, 2))
        self.assertIsNotNone(path)
        total_cost = get_path_cost(cost_grid, path)
        self.assertEqual(total_cost, 0.0)

    def test_create_cost_grid(self):
        grid = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0]
        ]
        cost_grid = create_cost_grid(grid, default_cost=2.0, wall_cost=-1.0)
        self.assertEqual(cost_grid[0][0], 2.0)  # 可通行
        self.assertEqual(cost_grid[0][1], -1.0)  # 障碍物
        self.assertEqual(cost_grid[1][1], 2.0)  # 可通行

    def test_create_cost_grid_custom(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        custom_costs = {(1, 1): 10.0}
        cost_grid = create_cost_grid(grid, custom_costs=custom_costs)
        self.assertEqual(cost_grid[1][1], 10.0)
        self.assertEqual(cost_grid[0][0], 1.0)

    def test_get_path_cost(self):
        cost_grid = [
            [1, 1, 1],
            [1, 5, 1],
            [1, 1, 1]
        ]
        path = astar_cost(cost_grid, (0, 0), (2, 2))
        self.assertIsNotNone(path)
        total_cost = get_path_cost(cost_grid, path)
        self.assertGreater(total_cost, 0)

    def test_get_path_cost_diagonal(self):
        cost_grid = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]
        path = astar_cost(cost_grid, (0, 0), (2, 2), allow_diagonal=True)
        self.assertIsNotNone(path)
        total_cost = get_path_cost(cost_grid, path, allow_diagonal=True)
        self.assertGreater(total_cost, 0)


if __name__ == '__main__':
    unittest.main()
