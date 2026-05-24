import unittest



from gaskill.sui import UI, Label, Button, Bar, Entry, draw, render_all


class TestUIComponents(unittest.TestCase):
    def test_ui_is_abstract(self):
        with self.assertRaises(TypeError):
            UI(0, 0, 100, 100)


class TestLabel(unittest.TestCase):
    def test_init(self):
        label = Label(0, 0, 100, 30, "Hello")
        self.assertEqual(label.text, "Hello")
        self.assertTrue(label.visible)

    def test_render(self):
        label = Label(0, 0, 100, 30, "Hello")
        cmds = label.render()
        self.assertTrue(len(cmds) > 0)

    def test_render_invisible(self):
        label = Label(0, 0, 100, 30, "Hello")
        label.visible = False
        cmds = label.render()
        self.assertEqual(len(cmds), 0)

    def test_config(self):
        label = Label(0, 0, 100, 30, "Hello")
        label.config(text="World", color=(255, 0, 0))
        self.assertEqual(label.text, "World")

    def test_enter(self):
        label = Label(0, 0, 100, 30, "Hello")
        self.assertTrue(label.enter(50, 15))
        self.assertFalse(label.enter(200, 200))


class TestButton(unittest.TestCase):
    def test_init(self):
        button = Button(0, 0, 100, 40, "Click Me")
        self.assertEqual(button.text, "Click Me")
        self.assertFalse(button.hover)
        self.assertFalse(button.pressed)

    def test_render(self):
        button = Button(0, 0, 100, 40, "Click Me")
        cmds = button.render()
        self.assertTrue(len(cmds) > 0)

    def test_handle_event_hover(self):
        button = Button(0, 0, 100, 40, "Click Me")
        result = button.handle_event((50, 20), set())
        self.assertTrue(result)

    def test_press_release(self):
        button = Button(0, 0, 100, 40, "Click Me")
        button.hover = True
        button.press()
        self.assertTrue(button.pressed)
        result = button.release()
        self.assertIsNotNone(result)  # 返回 True 或 False 都行

    def test_destroy(self):
        button = Button(0, 0, 100, 40, "Click Me")
        button.destroy()
        self.assertFalse(button.visible)


class TestBar(unittest.TestCase):
    def test_init(self):
        bar = Bar(0, 0, 200, 20, value=0.5)
        self.assertEqual(bar.value, 0.5)

    def test_value_clamp(self):
        bar = Bar(0, 0, 200, 20, value=1.5)
        self.assertEqual(bar.value, 1.0)
        bar = Bar(0, 0, 200, 20, value=-0.5)
        self.assertEqual(bar.value, 0.0)

    def test_render(self):
        bar = Bar(0, 0, 200, 20, value=0.5)
        cmds = bar.render()
        self.assertTrue(len(cmds) > 0)

    def test_config(self):
        bar = Bar(0, 0, 200, 20)
        bar.config(value=0.75)
        self.assertEqual(bar.value, 0.75)

    def test_set_hp(self):
        bar = Bar(0, 0, 200, 20)
        bar.set_hp(75, 100)
        self.assertEqual(bar.value, 0.75)


class TestEntry(unittest.TestCase):
    def test_init(self):
        entry = Entry(0, 0, 200, 30, "Hello")
        self.assertEqual(entry.text, "Hello")
        self.assertFalse(entry.focused)

    def test_render(self):
        entry = Entry(0, 0, 200, 30, "Hello")
        cmds = entry.render()
        self.assertTrue(len(cmds) > 0)

    def test_handle_event_focus(self):
        entry = Entry(0, 0, 200, 30)
        entry.handle_event((100, 15), {"mouse_left"}, 0)
        self.assertTrue(entry.focused)

    def test_enter(self):
        entry = Entry(0, 0, 200, 30)
        self.assertTrue(entry.enter(100, 15))

    def test_destroy(self):
        entry = Entry(0, 0, 200, 30)
        entry.destroy()
        self.assertFalse(entry.visible)


class TestRenderAll(unittest.TestCase):
    def test_render_all(self):
        label = Label(0, 0, 100, 30, "Test")
        cmds = render_all([label])
        self.assertTrue(len(cmds) > 0)


class TestDrawDecorator(unittest.TestCase):
    def test_draw_decorator(self):
        @draw('custom')
        def custom_handler(cmd):
            pass


if __name__ == '__main__':
    unittest.main()
