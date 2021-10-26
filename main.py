import math
import random
import pygame
from pygame.locals import *


debug = []
pygame.init()
clock = pygame.time.Clock()
frame_rate = 60

# Screen
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)

# Title
pygame.display.set_caption('Decision Tree Tool')

# Colors
black = [0, 0, 0]
white = [255, 255, 255]
light_grey = [200, 200, 200]
dark_grey = [75, 75, 75]
grey = [128, 128, 128]
red = [255, 0, 0]
blue = [0, 200, 255]

# Font
default_font = 'Georgia'

# Static variables
bg_color = dark_grey
integers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
alpha_numeric = []
for item in integers:
    alpha_numeric.append(item)
for item in letters:
    alpha_numeric.append(item)
for item in capital_letters:
    alpha_numeric.append(item)


class Node:
    def __init__(self, x_pos: int, y_pos: int, label='', parents=None, children=None, radius=10,
                 font=default_font, font_size=20, held=False):
        ran = ''
        for _ in range(0, 30):
            ran += alpha_numeric[random.randint(0, len(alpha_numeric) - 1)]
        self.id = ran
        self.x = x_pos
        self.y = y_pos
        self.radius = radius
        self.label = label
        self.color = blue
        self.font = pygame.font.SysFont(font, font_size)
        self.show_label = True
        self.held = held
        self.selected = False
        self.held_offset = [0, 0]
        self.draw_edge = False
        self.type = 'node'
        if parents is None:
            self.parents = []
        else:
            self.parents = parents
        if children is None:
            self.children = []
        else:
            self.children = children

    def update_pos(self, pos: tuple):
        for node in tree.nodes:
            if node != self:
                if pos[0] - self.radius <= node.x <= pos[0] + self.radius:
                    if pos[1] - self.radius <= node.y <= pos[1] + self.radius:
                        return
        if self.held:
            self.x = pos[0] + self.held_offset[0]
            self.y = pos[1] + self.held_offset[1]
        else:
            self.x = pos[0]
            self.y = pos[1]

    def draw(self, offset=(0, 0)):
        if self.selected:
            pygame.draw.circle(screen, red, (self.x - offset[0], self.y - offset[1]), self.radius)
            pygame.draw.circle(screen, self.color, (self.x - offset[0], self.y - offset[1]), self.radius - 2)
        else:
            pygame.draw.circle(screen, black, (self.x - offset[0], self.y - offset[1]), self.radius)
            pygame.draw.circle(screen, self.color, (self.x - offset[0], self.y - offset[1]), self.radius - 2)
        if self.show_label:
            label = self.font.render(self.label, True, self.color)
            label_x = int(label.get_rect().width / 2)
            screen.blit(label, (self.x - label_x - offset[0], self.y - self.radius - 25 - offset[1]))


class Edge:
    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int, source: object, width=3, target=None,
                 held=False, label='', font=default_font, font_size=20):
        ran = ''
        for _ in range(0, 30):
            ran += alpha_numeric[random.randint(0, len(alpha_numeric) - 1)]
        self.id = ran
        self.label = label
        self.show_label = True
        self.color = black
        self.font = pygame.font.SysFont(font, font_size)
        self.font_size = font_size
        self.x = start_x
        self.y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.center = (0, 0)
        self.arrow_pos = (0.4, 0.6)
        self.width = width
        self.held = held
        self.selected = False
        self.parent = source
        self.child = target
        self.type = 'edge'

        # for IDE
        if self.x is None:
            self.parent = Node(0, 0)
            self.child = Node(0, 0)

    def draw(self, offset=(0, 0)):
        # Draw line
        pygame.draw.line(screen, self.color, (self.x - offset[0], self.y - offset[1]),
                         (self.end_x - offset[0], self.end_y - offset[1]), self.width)
        if self.selected:
            pygame.draw.line(screen, red, (self.x - offset[0], self.y - offset[1]),
                             (self.end_x - offset[0], self.end_y - offset[1]), 1)

        # Draw Arrow
        p = self.arrow_pos
        middle = (int(p[0] * self.x + p[1] * self.end_x) - offset[0],
                  int(p[0] * self.y + p[1] * self.end_y) - offset[1])
        rotation = math.degrees(math.atan2(self.y - self.end_y, self.end_x - self.x)) + 90
        plus = 165
        times = 20
        if not self.selected:
            pygame.draw.polygon(screen, self.color, (middle,
                                                     (int(middle[0] + times * math.sin(math.radians(rotation - plus))),
                                                      int(middle[1] + times * math.cos(math.radians(rotation - plus)))),
                                                     (int(middle[0] + times * math.sin(math.radians(rotation + plus))),
                                                      int(middle[1] + times * math.cos(math.radians(rotation + plus)))))
                                )
        else:
            pygame.draw.polygon(screen, red, (middle,
                                              (int(middle[0] + times * math.sin(math.radians(rotation - plus))),
                                               int(middle[1] + times * math.cos(math.radians(rotation - plus)))),
                                              (int(middle[0] + times * math.sin(math.radians(rotation + plus))),
                                               int(middle[1] + times * math.cos(math.radians(rotation + plus))))))

        # Draw label
        if self.show_label:
            label = self.font.render(self.label, True, white)
            label_x = int(label.get_rect().width / 2)
            screen.blit(label, (self.center[0] - label_x - offset[0],
                                self.center[1] - label.get_rect().height - offset[1]))

    def update_pos(self, pos=None):
        if pos is None:
            if self.parent is not None:
                self.x = self.parent.x
                self.y = self.parent.y
            if self.child is not None:
                self.end_x = self.child.x
                self.end_y = self.child.y
        else:
            self.end_x = pos[0]
            self.end_y = pos[1]

        p = self.arrow_pos
        self.center = (int(p[0] * self.x + p[1] * self.end_x), int(p[0] * self.y + p[1] * self.end_y))

    def check_collide(self, pos: tuple):
        if self.center[0] - 20 <= pos[0] <= self.center[0] + 20:
            if self.center[1] - 20 <= pos[1] <= self.center[1] + 20:
                return True
        return False


class Tree:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.menu = Menu(0, 0)
        self.view_offset = (0, 0)

    def draw_screen(self):
        global view_drag_temp
        global view_drag

        screen.fill(bg_color)
        if not view_drag:
            for edge in self.edges:
                # Relocate pos update function
                edge.update_pos()
                edge.draw()
            for node in self.nodes:
                node.draw()
        else:
            for edge in self.edges:
                # Relocate pos update function
                edge.update_pos()
                edge.draw(offset=(view_drag_temp[0], view_drag_temp[1]))
            for node in self.nodes:
                node.draw(offset=(view_drag_temp[0], view_drag_temp[1]))

        self.menu.draw()

    def save_tree(self):
        save_file = open('tree_' + ran_name + '.txt', 'w', errors='ignore')
        text = '**NODES**\n'
        for item in self.nodes:
            text += str(item.id) + '\n' + str(item.label) + '\n' + str(item.x) + '\n' + str(item.y) + '\n' +\
                    'parents\n'
            for parent in item.parents:
                text += parent.id + '\n'
            text += 'parents' + '\n' + 'children' + '\n'
            for child in item.children:
                text += child.id + '\n'
            text += 'children\n'
        text += '**EDGES**\n'
        for item in self.edges:
            text += item.parent.id + '\n' + item.child.id + '\n' + item.label + '\n'
        save_file.writelines(text)
        save_file.close()


class Button:
    def __init__(self, x: int, y: int, label: str, padding=5, border_width=2, border_color=None, border_off=False,
                 button_color=None, font=default_font, font_size=20, font_color=None, action=None, highlight=False):
        if action is None:
            self.action = ''
        else:
            self.action = action
        if border_color is None:
            border_color = light_grey
        if font_color is None:
            font_color = light_grey
        self.type = 'button'
        self.x = x
        self.y = y
        self.padding = padding
        self.color = button_color
        self.font = pygame.font.SysFont(font, font_size)
        self.label = self.font.render(label, True, font_color)
        self.pressed_label = self.font.render(label, True, blue)
        self.label_width = int(self.label.get_rect().width)
        self.label_height = int(self.label.get_rect().height)
        self.width = self.label_width + self.padding * 2
        self.height = self.label_height + self.padding * 2
        self.border = border_width
        self.border_color = border_color
        self.border_color_pressed = blue
        self.border_off = border_off
        self.run = False
        self.pressed = False
        self.pressed_draw = False
        self.highlight_when_hover = highlight

    def draw(self):
        if not self.pressed_draw:
            if self.color is not None:
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            self.draw_border()
            screen.blit(self.label, (self.x + self.padding, self.y + self.padding))
        else:
            if self.color is not None:
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            self.draw_border()
            screen.blit(self.pressed_label, (self.x + self.padding, self.y + self.padding))

    def draw_border(self):
        if not self.border_off:
            if not self.pressed_draw:
                pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.border, self.height))
                pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.border))
                pygame.draw.rect(screen, self.border_color, (self.x, self.y + self.height - self.border, self.width,
                                                             self.border))
                pygame.draw.rect(screen, self.border_color, (self.x + self.width - self.border,
                                                             self.y, self.border, self.height))
            else:
                pygame.draw.rect(screen, self.border_color_pressed, (self.x, self.y, self.border, self.height))
                pygame.draw.rect(screen, self.border_color_pressed, (self.x, self.y, self.width, self.border))
                pygame.draw.rect(screen, self.border_color_pressed, (self.x, self.y + self.height - self.border,
                                                                     self.width, self.border))
                pygame.draw.rect(screen, self.border_color_pressed, (self.x + self.width - self.border,
                                                                     self.y, self.border, self.height))

    def check_collide(self, pos: tuple):
        if self.x <= pos[0] <= self.x + self.width:
            if self.y <= pos[1] <= self.y + self.height:
                return True
        return False

    def mouse_input(self, pos: tuple, mouse: tuple, pressed: str):
        global left_mouse_held
        collided = self.check_collide(pos)

        if left_mouse_held and self.pressed:
            if collided:
                self.pressed_draw = True
            else:
                self.pressed_draw = False

        if pressed == 'down':
            if collided and mouse[0]:
                self.pressed = True
                self.pressed_draw = True
        elif pressed == 'up':
            if collided and self.pressed and not mouse[0]:
                self.run = True

        if self.highlight_when_hover:
            if collided:
                self.pressed_draw = True
            else:
                self.pressed_draw = False

    def update_pos(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]


class TextBox:
    def __init__(self, x_pos, y_pos, label='', text='', padding=5, border_width=2, selected=False, clear_on_init=False):
        self.type = 'textbox'
        self.color = light_grey
        self.bg_color = bg_color
        self.border_color = self.color
        self.border_width = border_width
        self.x = x_pos
        self.y = y_pos
        self.padding = padding
        self.text = text
        self.font = pygame.font.SysFont(default_font, 20)
        self.label = label
        if label == '':
            self.label_offset = 0
        else:
            self.label_offset = int(self.font.render(self.label, True, self.color).get_rect().width) + 5
        self.text_width = int(self.font.render(self.text, True, self.color).get_rect().width)
        self.text_height = int(self.font.render(self.text, True, self.color).get_rect().height)
        self.min_width = self.text_width + self.padding * 2 + 5
        self.width = self.min_width
        self.height = self.text_height + self.padding * 2

        self.selected = selected
        self.cursor_pos = self.text_width + self.x + self.padding + 2
        self.blink_counter = 0
        self.text_input_counter = 0
        if clear_on_init:
            self.update_text(character='clear', backspace=True)

    def draw(self):
        # Label
        screen.blit(self.font.render(self.label + ':', True, self.color), (self.x, self.y + self.padding))

        # Left edge
        pygame.draw.rect(screen, self.border_color, (self.x + self.label_offset, self.y, self.border_width,
                                                     self.height))
        # Top edge
        pygame.draw.rect(screen, self.border_color, (self.x + self.label_offset, self.y, self.width, self.border_width))
        # Bottom edge
        pygame.draw.rect(screen, self.border_color, (self.x + self.label_offset,
                                                     self.y + self.height - self.border_width, self.width,
                                                     self.border_width))
        # Right edge
        pygame.draw.rect(screen, self.border_color, (self.x + self.label_offset + self.width - self.border_width,
                                                     self.y, self.border_width, self.height))

        # Text
        screen.blit(self.font.render(self.text, True, self.color), (self.x + self.label_offset + self.padding,
                                                                    self.y + self.padding))

        # Draw Cursor
        if self.selected:
            if self.text_input_counter == 0:
                if -25 <= self.blink_counter <= 0:
                    pygame.draw.rect(screen, red, (self.cursor_pos + self.label_offset, self.y + self.padding, 3,
                                                   self.height - self.padding * 2))
                elif self.blink_counter <= -25:
                    self.blink_counter = 26
                self.blink_counter -= 1
            else:
                if self.text_input_counter > 0:
                    self.text_input_counter -= 1
                else:
                    self.text_input_counter = 0
                pygame.draw.rect(screen, red, (self.cursor_pos + self.label_offset, self.y + self.padding, 3,
                                               self.height - self.padding * 2))

    def update_text(self, character='', backspace=False):
        if character == 'clear' and backspace:
            self.text = ''
        else:
            self.text += character
            self.text_input_counter = int(frame_rate * 1.5)
        self.blink_counter = 0
        if backspace:
            self.text = self.text[:-1]
        self.text_width = int(self.font.render(self.text, True, self.color).get_rect().width)
        new_width = self.text_width + self.padding * 2 + 5
        if new_width >= self.min_width:
            self.width = new_width
        self.cursor_pos = self.text_width + self.x + self.padding + 2

    def clear_text(self):
        self.update_text('clear', backspace=True)

    def check_collide(self, pos: tuple):
        if self.x + self.label_offset + self.padding <= pos[0] <=\
                self.x + self.width + self.label_offset + self.padding:
            if self.y <= pos[1] <= self.y + self.height:
                return True
        return False

    def update_pos(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]
        self.cursor_pos = self.text_width + self.x + self.padding + 2


class Menu:
    def __init__(self, x_pos: int, y_pos: int, source=None):
        self.source = source
        self.x = x_pos
        self.y = y_pos
        self.width = 250
        self.height = screen_height
        self.padding = 7
        self.border_width = 2
        self.items = []

        # for IDE
        if self.x is None:
            self.source = Node(0, 0)

        y_offset = 45
        width = 0
        if source is None:
            self.items = [Button(self.x + self.padding, self.y + self.padding,
                                 'Create New Node', action='node')]
            width = self.items[0].width + self.padding
            self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                      label='Label', text=''))
            y_offset += self.items[0].height + self.padding
            self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                      label='Children', text=''))
            for item in self.items:
                if item.type == 'textbox':
                    if item.width + item.label_offset > width:
                        width = item.width + item.label_offset
        self.width = width + self.padding * 2
        for item in self.items:
            if item.type == 'textbox':
                if item.x + item.width + item.label_offset != width:
                    item.width += width - item.width - item.label_offset
                    item.min_width = item.width

    def draw(self):
        tree.menu.refresh_data()

        for item in self.items:
            item.draw()

        # Left edge
        pygame.draw.rect(screen, light_grey, (self.x, self.y, self.border_width, self.height))
        # Top edge
        pygame.draw.rect(screen, light_grey, (self.x, self.y, self.width, self.border_width))
        # Bottom edge
        pygame.draw.rect(screen, light_grey, (self.x, self.y + self.height - self.border_width, self.width,
                                              self.border_width))
        # Right edge
        pygame.draw.rect(screen, light_grey, (self.x + self.width - self.border_width,
                                              self.y, self.border_width, self.height))

    def update_source(self, source: object):
        # For IDE
        if self.x is None:
            source = Node(0, 0)

        if source is not None:
            if self.source is None:
                self.source = source
            else:
                self.source.selected = False
                y_offset = 45
                if source.type == self.source.type:
                    self.refresh_data()

                elif source.type == 'node':
                    self.items = [Button(self.x + self.padding, self.y + self.padding,
                                         'Create New Node', action='node')]
                    self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                              label='Label', text=''))
                    y_offset += self.items[0].height + self.padding
                    self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                              label='Children', text=''))

                    for item in self.items:
                        if item.type == 'textbox':
                            if item.x + item.width + item.label_offset != self.width - self.padding * 2:
                                item.width += self.width - self.padding * 2 - item.width - item.label_offset
                                item.min_width = item.width

                elif source.type == 'edge':
                    self.items = [(TextBox(self.x + self.padding, self.y + y_offset,
                                           label='Label', text=source.label))]

                    for item in self.items:
                        if item.type == 'textbox':
                            if item.x + item.width + item.label_offset != self.width - self.padding * 2:
                                item.width += self.width - self.padding * 2 - item.width - item.label_offset
                                item.min_width = item.width

            source.selected = True
            self.source = source
            for item in self.items:
                if item.type == 'textbox' and item.label == 'Label':
                    item.selected = True
        else:
            y_offset = 45
            self.items = [Button(self.x + self.padding, self.y + self.padding,
                                 'Create New Node', action='node')]
            self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                      label='Label', text=''))
            y_offset += self.items[0].height + self.padding
            self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                      label='Children', text=''))
            for item in self.items:
                if item.type == 'textbox':
                    if item.x + item.width + item.label_offset != self.width - self.padding * 2:
                        item.width += self.width - item.width - item.label_offset - self.padding * 2
                        item.min_width = item.width

    def refresh_data(self):
        if self.source is not None:
            for item in self.items:
                if item.type == 'textbox':
                    if item.label == 'Label':
                        if self.source.label != item.text:
                            item.clear_text()
                            item.update_text(self.source.label)
                    elif self.source.type == 'node' and item.label == 'Children':
                        if str(len(self.source.children)) != item.text:
                            item.clear_text()
                            item.update_text(str(len(self.source.children)))


# Box drag select for group move, Zoom function (deceptively hard)
# Fix menu generally, textbox scrolling
# Save to file, reorganize everything


def mouse_handler(event_type: str, mouse_pos: tuple, mouse_buttons: tuple):
    global left_mouse_held
    global right_mouse_held
    global view_drag
    global orig_mouse_pos
    global view_drag_temp
    global tree
    global draw_edge
    global double_click
    global double_click_timer

    def create_new_node():
        global auto_name

        if auto_name == '':
            auto_name = 'A'
        elif len(auto_name) == 1 and auto_name != 'Z':
            auto_name = capital_letters[capital_letters.index(auto_name) + 1]
        elif len(auto_name) == 1 and auto_name == 'Z':
            auto_name = 'AA'
        else:
            index = 0
            for i in reversed(range(len(auto_name))):
                index += 1
                if auto_name[i] == 'Z':
                    if i == 0:
                        length = len(auto_name)
                        auto_name = ''
                        for _ in range(0, length + 1):
                            auto_name += 'A'
                else:
                    auto_name = auto_name[:i] + capital_letters[capital_letters.index(auto_name[i]) + 1]
                    for _ in range(0, index - 1):
                        auto_name += 'A'
                    break

        for node in tree.nodes:
            if auto_name == node.label:
                create_new_node()
                return

        tree.nodes.append(Node(mouse_pos[0] - tree.view_offset[0], mouse_pos[1] - tree.view_offset[1],
                               held=True, label=auto_name))
        tree.menu.update_source(tree.nodes[-1])

    distance_to_node = 0
    for node in tree.nodes:
        if node.draw_edge:
            distance_to_node = ((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2)**0.5

    if event_type == 'down':
        for item in tree.menu.items:
            if item.type == 'button':
                item.mouse_input(mouse_pos, mouse_buttons, 'down')
        # Left click
        if mouse_buttons[0]:
            left_mouse_held = True

            node_click = False
            # Left click node
            for node in tree.nodes:
                if ((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2)**0.5 <= node.radius + 1:
                    node_click = True
                    node.held_offset = [node.x - mouse_pos[0], node.y - mouse_pos[1]]
                    node.held = True
                    tree.menu.update_source(node)
            # Left click background
            if not node_click:
                # Select Edge
                edge_click = False
                for edge in tree.edges:
                    if edge.check_collide(mouse_pos):
                        tree.menu.update_source(edge)
                        edge_click = True

                # Select menu item
                if not edge_click:
                    menu_click = False
                    for item in tree.menu.items:
                        if item.type == 'textbox':
                            item.blink_counter = 0
                            item.selected = False
                            if item.check_collide(mouse_pos):
                                item.selected = True
                                menu_click = True

                    # Enable view drag
                    if not menu_click:
                        view_drag = True

                        if double_click and double_click_timer > 0:
                            create_new_node()
                            double_click_timer = 0
                            double_click = False
                            view_drag = False

                        if view_drag:
                            view_drag_temp = tree.view_offset
                            orig_mouse_pos = mouse_pos

            if not double_click:
                double_click = True
                double_click_timer = int(frame_rate / 3)

        # Right click
        if mouse_buttons[2]:
            right_mouse_held = True
            node_click = False
            # Right click node
            for node in tree.nodes:
                if ((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2)**0.5 <= node.radius + 1:
                    node_click = True
                    if not draw_edge:
                        node.draw_edge = True
                    break
            # Right click background
            if not node_click:
                if draw_edge:
                    create_new_node()
    elif event_type == 'up':
        for item in tree.menu.items:
            if item.type == 'button':
                item.mouse_input(mouse_pos, mouse_buttons, 'up')
        # Left unclick
        if not mouse_buttons[0]:
            view_drag = False
            tree.view_offset = (tree.view_offset[0] + view_drag_temp[0], tree.view_offset[1] + view_drag_temp[1])
            for node in tree.nodes:
                node.x = node.x - view_drag_temp[0]
                node.y = node.y - view_drag_temp[1]
            for edge in tree.edges:
                edge.update_pos()
            view_drag_temp = (0, 0)
            left_mouse_held = False
            for node in tree.nodes:
                node.held = False

        # Right unclick
        if not mouse_buttons[2]:
            right_mouse_held = False
            for node in tree.nodes:
                if ((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2)**0.5 <= node.radius + 1:
                    if draw_edge:
                        edge = tree.edges[-1]
                        if node not in edge.parent.children:
                            draw_edge = False
                            edge.parent.draw_edge = False
                            edge.held = False
                            edge.child = node
                            edge.update_pos()
                            if edge.label == '':
                                edge.label = edge.parent.label + '>' + edge.child.label
                            # Update nodes data
                            edge.parent.children.append(edge.child)
                            edge.child.parents.append(edge.parent)

                    # Open Node data menu
                    elif node.draw_edge:
                        node.draw_edge = False
                    break

    # Button actions
    for item in tree.menu.items:
        if item.type == 'button':
            if item.run:
                if item.action == 'node':
                    create_new_node()
                item.run = False
            else:
                item.mouse_input(mouse_pos, mouse_buttons, '')

    # Nodes / Edges
    for node in tree.nodes:
        if node.held:
            node.update_pos(mouse_pos)
        elif not draw_edge and node.draw_edge:
            if abs(distance_to_node) >= node.radius + 5:
                tree.edges.append(Edge(node.x - tree.view_offset[0], node.y - tree.view_offset[1], 0, 0, node))
                draw_edge = True
        elif node.draw_edge:
            if abs(distance_to_node) <= node.radius + 1:
                draw_edge = False
                tree.edges.pop()
    if draw_edge:
        tree.edges[-1].update_pos(mouse_pos)

    # View drag
    if view_drag:
        view_drag_temp = (orig_mouse_pos[0] - mouse_pos[0], orig_mouse_pos[1] - mouse_pos[1])


def zoom_tree(delta_zoom: int):
    global zoom
    global zoom_factor

    zoom += delta_zoom
    if zoom > 0:
        zoom_factor = 1 + delta_zoom * 0.1
    elif zoom < 0:
        zoom_factor = 1 + delta_zoom * 0.05
    else:
        zoom_factor = 1

    # for node in tree.nodes:
    #     theta = math.atan2((node.y - (screen_height / 2)), (node.x - (screen_width / 2)))
    #     if theta < 0:
    #         theta = math.radians(360) + theta
    #     d = math.sqrt((node.y - (screen_height / 2))**2 + (node.x - (screen_width / 2))**2) + math.sqrt(2)
    #     x = (math.cos(theta) * d) + (screen_width / 2)
    #     y = (math.sin(theta) * d) + (screen_height / 2)
    #     node.update_pos((x, y))


def debug_(variables: list):
    global debug

    if debug != variables:
        debug = variables
        print(debug)


tree = Tree()
ran_name = ''
for _ in range(0, 10):
    ran_name += alpha_numeric[random.randint(0, len(alpha_numeric) - 1)]

# Maybe label these
delete_item = False
delete_timer = 0
left_mouse_held = False
double_click = False
auto_name = ''
double_click_timer = 0
right_mouse_held = False
view_drag = False
orig_mouse_pos = (0, 0)
view_drag_temp = (0, 0)
zoom = 0
zoom_factor = 1
draw_edge = False
held_key = ''
held_key_event = None
key_hold_counter = 0
running = True
while running:
    tree.draw_screen()
    # Event loop
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        # Close window
        if event.type == QUIT:
            running = False
            break

        # Key down events
        elif event.type == KEYDOWN:
            # Close window shortcut
            if (keys[K_LCTRL] or keys[K_RCTRL]) and keys[K_w]:
                running = False
                break

            # Return to original view position
            if (keys[K_LCTRL] or keys[K_RCTRL]) and keys[K_o]:
                for node in tree.nodes:
                    node.x += tree.view_offset[0]
                    node.y += tree.view_offset[1]
                tree.view_offset = (0, 0)

            # Save tree
            if (keys[K_LCTRL] or keys[K_RCTRL]) and keys[K_s]:
                tree.save_tree()

            # Send input to Menu textbox
            for m_item in tree.menu.items:
                if m_item.type == 'textbox':
                    if tree.menu.source is not None and m_item.selected:
                        if keys[K_BACKSPACE]:
                            held_key = 'backspace'
                            key_hold_counter = int(frame_rate)
                            m_item.update_text(backspace=True)
                        elif m_item.label == 'Children':
                            if event.unicode in integers:
                                held_key = event.unicode
                                held_key_event = event
                                key_hold_counter = int(frame_rate)
                                m_item.update_text(event.unicode)
                        else:
                            held_key = event.unicode
                            held_key_event = event
                            key_hold_counter = int(frame_rate)
                            m_item.update_text(event.unicode)

                        # update node data
                        if m_item.label == 'Label':
                            tree.menu.source.label = m_item.text

            # Delete selected item
            if keys[K_DELETE]:
                if not delete_item:
                    delete_item = True
                    delete_timer = int(frame_rate / 2)
                elif delete_timer > 0:
                    if tree.menu.source is not None:
                        if tree.menu.source.type == 'node':
                            if len(tree.menu.source.parents) != 0:
                                for parent in tree.menu.source.parents:
                                    parent.children.pop(parent.children.index(tree.menu.source))
                            if len(tree.menu.source.children) != 0:
                                for child in tree.menu.source.children:
                                    child.parents.pop(child.parents.index(tree.menu.source))
                            if len(tree.menu.source.parents) != 0 or len(tree.menu.source.children) != 0:
                                pop_list = []
                                for edge in tree.edges:
                                    if edge.parent == tree.menu.source or edge.child == tree.menu.source:
                                        pop_list.append(tree.edges.index(edge))
                                pop_list.sort(reverse=True)
                                for i in range(len(pop_list)):
                                    tree.edges.pop(pop_list[i])
                            tree.nodes.pop(tree.nodes.index(tree.menu.source))
                        elif tree.menu.source.type == 'edge':
                            # For IDE
                            if delete_timer < 0:
                                edge = Edge(0, 0, 0, 0, None)
                            else:
                                edge = tree.menu.source

                            edge.parent.children.pop(edge.parent.children.index(edge.child))
                            edge.child.parents.pop(edge.child.parents.index(edge.parent))
                            tree.edges.pop(tree.edges.index(edge))

                    tree.menu.update_source(None)
                    delete_item = False

        # Key up events
        elif event.type == KEYUP:
            if held_key != '':
                if held_key == 'backspace' and not keys[K_BACKSPACE]:
                    held_key = ''
                elif held_key_event is not None:
                    if held_key == held_key_event.unicode and event not in keys:
                        held_key = ''
                        held_key_event = None

        # Mouse down event
        elif event.type == MOUSEBUTTONDOWN:
            mouse_handler('down', pygame.mouse.get_pos(), pygame.mouse.get_pressed())

        # Mouse up event
        elif event.type == MOUSEBUTTONUP:
            mouse_handler('up', pygame.mouse.get_pos(), pygame.mouse.get_pressed())

        elif event.type == MOUSEWHEEL:
            if not event.flipped:
                zoom_tree(event.y)
            else:
                zoom_tree(- event.y)

        # Resize
        elif event.type == VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
            tree.menu.height = screen_height

    mouse_handler('', pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    # Timers
    if held_key != '' and key_hold_counter == 0:
        key_hold_counter = int(frame_rate / 30)
        for m_item in tree.menu.items:
            if m_item.type == 'textbox':
                if m_item.selected:
                    if held_key == 'backspace':
                        m_item.update_text(backspace=True)
                    else:
                        m_item.update_text(held_key)
                # Update source object
                    if m_item.label == 'Label':
                        tree.menu.source.label = m_item.text
                    break
    elif key_hold_counter > 0:
        key_hold_counter -= 1

    # Double press to delete
    if delete_item and delete_timer > 0:
        delete_timer -= 1
        if delete_timer == 0:
            delete_item = False

    # Double click
    if double_click and double_click_timer > 0:
        double_click_timer -= 1
        if double_click_timer == 0:
            double_click = False

    clock.tick(frame_rate)
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
