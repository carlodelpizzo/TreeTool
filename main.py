import math
import random
import pygame
from pygame.locals import *
import os


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
red = [220, 30, 0]
green = [0, 215, 100]
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
for item_ in integers:
    alpha_numeric.append(item_)
for item_ in letters:
    alpha_numeric.append(item_)
for item_ in capital_letters:
    alpha_numeric.append(item_)

ran_name = ''
old_ran = ''
for _ in range(0, 10):
    ran_name += alpha_numeric[random.randint(0, len(alpha_numeric) - 1)]


class Node:
    def __init__(self, x_pos: int, y_pos: int, label='', parents=None, children=None, radius=10,
                 font=default_font, font_size=20, held=False, node_id=None):
        if node_id is None:
            ran = ''
            for _ in range(0, 30):
                ran += alpha_numeric[random.randint(0, len(alpha_numeric) - 1)]
            node_id = ran
        self.id = node_id
        self.x = x_pos
        self.y = y_pos
        self.radius = radius
        self.label = label
        self.color = blue
        self.font = pygame.font.SysFont(font, font_size)
        self.show_label = True
        self.held = held
        self.selected = False
        self.sourced = False
        self.held_offset = [0, 0]
        self.draw_edge = False
        self.type = 'node'
        self.deleted = False

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
        if self.sourced:
            pygame.draw.circle(screen, red, (self.x - offset[0], self.y - offset[1]), self.radius)
            pygame.draw.circle(screen, self.color, (self.x - offset[0], self.y - offset[1]), self.radius - 2)
        else:
            pygame.draw.circle(screen, black, (self.x - offset[0], self.y - offset[1]), self.radius)
            pygame.draw.circle(screen, self.color, (self.x - offset[0], self.y - offset[1]), self.radius - 2)
        if self.show_label:
            label = self.font.render(self.label, True, self.color)
            label_x = int(label.get_rect().width / 2)
            screen.blit(label, (self.x - label_x - offset[0], self.y - self.radius - 25 - offset[1]))

        if self.selected:
            pygame.draw.circle(screen, red, (self.x - offset[0], self.y - offset[1]), int(self.radius / 2))


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
        self.sourced = False
        self.parent = source
        self.child = target
        self.type = 'edge'
        self.deleted = False

        # for IDE
        if self.x is None:
            self.parent = Node(0, 0)
            self.child = Node(0, 0)

    def draw(self, offset=(0, 0)):
        # Draw line
        pygame.draw.line(screen, self.color, (self.x - offset[0], self.y - offset[1]),
                         (self.end_x - offset[0], self.end_y - offset[1]), self.width)
        if self.sourced:
            pygame.draw.line(screen, red, (self.x - offset[0], self.y - offset[1]),
                             (self.end_x - offset[0], self.end_y - offset[1]), 1)

        # Draw Arrow
        p = self.arrow_pos
        middle = (int(p[0] * self.x + p[1] * self.end_x) - offset[0],
                  int(p[0] * self.y + p[1] * self.end_y) - offset[1])
        rotation = math.degrees(math.atan2(self.y - self.end_y, self.end_x - self.x)) + 90
        plus = 165
        times = 20
        if not self.sourced:
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

    def draw_label(self, offset=(0, 0)):
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
        self.selection_box = None

        # For IDE
        if self.selection_box is not None:
            self.selection_box = SelectionBox(0, 0)

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
            if self.selection_box is not None:
                self.selection_box.draw()
            for edge in self.edges:
                edge.draw_label()
        else:
            for edge in self.edges:
                # Relocate pos update function
                edge.update_pos()
                edge.draw(offset=(view_drag_temp[0], view_drag_temp[1]))
            for node in self.nodes:
                node.draw(offset=(view_drag_temp[0], view_drag_temp[1]))
            if self.selection_box is not None:
                self.selection_box.draw(offset=(view_drag_temp[0], view_drag_temp[1]))
            for edge in self.edges:
                edge.draw_label(offset=(view_drag_temp[0], view_drag_temp[1]))

        if len(tree.nodes) < 3:
            if len(tree.nodes) == 0:
                temp_label = Label(0, 0, 'Double Click to Create New Node', font_size=30)
                temp_label.x = int(((screen_width - tree.menu.width) / 2) - (temp_label.width / 2)) + tree.menu.width
                temp_label.y = int((screen_height / 2) - (temp_label.height / 2))
                temp_label.draw()
            elif len(tree.nodes) == 1:
                if len(tree.edges) == 0:
                    if not tree.nodes[0].draw_edge:
                        temp_label = Label(0, 0, 'Right Click Node to Create Edge', font_size=30)
                        temp_label.x = int(((screen_width - tree.menu.width) / 2) - (temp_label.width / 2))
                        temp_label.x += tree.menu.width
                        temp_label.y = int(screen_height - temp_label.height - 5)
                        temp_label.draw()
                    elif tree.nodes[0].draw_edge:
                        temp_label = Label(0, 0, 'Move Mouse to Draw Edge', font_size=30)
                        temp_label.x = int(((screen_width - tree.menu.width) / 2) - (temp_label.width / 2))
                        temp_label.x += tree.menu.width
                        temp_label.y = int(screen_height - temp_label.height - 5)
                        temp_label.draw()
                elif len(tree.edges) == 1:
                    temp_label = Label(0, 0, 'Right Click Again to Create New Node', font_size=30)
                    temp_label.x = int(((screen_width - tree.menu.width) / 2) - (temp_label.width / 2))
                    temp_label.x += tree.menu.width
                    temp_label.y = int(screen_height - temp_label.height - 5)
                    temp_label.draw()
            elif len(tree.nodes) == 2:
                if len(tree.edges) == 0:
                    if not (tree.nodes[0].draw_edge or tree.nodes[1].draw_edge):
                        temp_label = Label(0, 0, 'Right Click Node to Create Edge', font_size=30)
                        temp_label.x = int(((screen_width - tree.menu.width) / 2) - (temp_label.width / 2))
                        temp_label.x += tree.menu.width
                        temp_label.y = int(screen_height - temp_label.height - 5)
                        temp_label.draw()
                    elif tree.nodes[0].draw_edge or tree.nodes[1].draw_edge:
                        temp_label = Label(0, 0, 'Move Mouse to Draw Edge', font_size=30)
                        temp_label.x = int(((screen_width - tree.menu.width) / 2) - (temp_label.width / 2))
                        temp_label.x += tree.menu.width
                        temp_label.y = int(screen_height - temp_label.height - 5)
                        temp_label.draw()
                elif len(tree.edges) == 1 and (tree.nodes[0].draw_edge or tree.nodes[1].draw_edge) and draw_edge:
                    temp_label = Label(0, 0, 'Right Click on Another Node to Connect', font_size=30)
                    temp_label.x = int(((screen_width - tree.menu.width) / 2) - (temp_label.width / 2))
                    temp_label.x += tree.menu.width
                    temp_label.y = int(screen_height - temp_label.height - 5)
                    temp_label.draw()

        self.menu.draw()

    def save_tree(self):
        global loaded_file

        if loaded_file == '':
            save_file = open(ran_name + '.tree', 'w', errors='ignore')
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
        else:
            save_file = open(loaded_file, 'w', errors='ignore')
            save_file.truncate()
            text = '**NODES**\n'
            for item in self.nodes:
                text += str(item.id) + '\n' + str(item.label) + '\n' + str(item.x) + '\n' + str(item.y) + '\n' + \
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

    def load_tree(self, from_file=False, file_path=''):
        global ran_name
        global old_ran
        global loaded_file
        global loaded_name

        if not from_file:
            if os.path.isfile('load.tree'):
                if len(self.nodes) > 0:
                    self.save_tree()

                loaded_file = ''
                loaded_name = ''
                old_ran = ran_name
                ran_name = ''
                for _ in range(0, 10):
                    ran_name += alpha_numeric[random.randint(0, len(alpha_numeric) - 1)]

                for fixture in self.menu.fixtures:
                    if fixture.type == 'label':
                        if old_ran in fixture.label_text:
                            fixture.update_label(fixture.label_text.replace(old_ran, ran_name))

                tree.menu.resize()

                self.nodes = []
                self.edges = []
                self.menu.fixtures = []
                self.menu = Menu(0, 0)
                self.view_offset = (0, 0)
                self.selection_box = None

                save_file = open('load.tree', 'r', errors='ignore')
                load_nodes = False
                load_edges = False
                nodes = []
                node_temp = []
                edges = []
                edge_temp = []
                # Node format: 0 = id, 1 = label, 2 = x, 3 = y,
                # 4 = 'parents', ...,  n = 'parents, n+1 = 'children', ..., k = 'children'
                # Edge format: 0 = parent.id, 1 = child.id, 2 = label
                for line in save_file:
                    if '**NODES**' in line:
                        load_nodes = True
                        load_edges = False
                        continue
                    elif '**EDGES**' in line:
                        load_nodes = False
                        load_edges = True
                        continue
                    if load_nodes:
                        if 'children' in line:
                            if 'children' in node_temp:
                                node_temp.append(line.replace('\n', ''))
                                nodes.append(node_temp)
                                node_temp = []
                            else:
                                node_temp.append(line.replace('\n', ''))
                        else:
                            node_temp.append(line.replace('\n', ''))
                    elif load_edges:
                        edge_temp.append(line.replace('\n', ''))
                        if len(edge_temp) == 3:
                            edges.append(edge_temp)
                            edge_temp = []

                parents = False
                children = False
                node_dict = {}
                for node in nodes:
                    self.nodes.append(Node(int(node[2]), int(node[3]), label=node[1], node_id=node[0]))
                    node_dict[node[0]] = self.nodes[-1]
                for node in nodes:
                    for i in range(4, len(node)):
                        if not parents and node[i] == 'parents':
                            parents = True
                            children = False
                            continue
                        elif parents and node[i] == 'parents':
                            parents = False
                        elif parents and node[i] != 'parents':
                            node_dict[node[0]].parents.append(node_dict[node[i]])
                        elif not children and node[i] == 'children':
                            parents = False
                            children = True
                            continue
                        elif children and node[i] != 'children':
                            node_dict[node[0]].children.append(node_dict[node[i]])

                for edge in edges:
                    source = node_dict[edge[0]]
                    target = node_dict[edge[1]]
                    self.edges.append(Edge(source.x, source.y, target.x, target.y, source,
                                           target=target, label=edge[2]))
                save_file.close()
        else:
            if os.path.isfile(file_path) and os.path.splitext(file_path)[1] == '.tree':
                if len(self.nodes) != 0:
                    self.save_tree()

                loaded_file = file_path
                loaded_name = os.path.basename(file_path)[:-len('.tree')]

                tree.menu.resize()

                self.nodes = []
                self.edges = []
                self.menu.fixtures = []
                self.menu = Menu(0, 0)
                self.view_offset = (0, 0)
                self.selection_box = None

                save_file = open(file_path, 'r', errors='ignore')
                load_nodes = False
                load_edges = False
                nodes = []
                node_temp = []
                edges = []
                edge_temp = []
                # Node format: 0 = id, 1 = label, 2 = x, 3 = y,
                # 4 = 'parents', ...,  n = 'parents, n+1 = 'children', ..., k = 'children'
                # Edge format: 0 = parent.id, 1 = child.id, 2 = label
                for line in save_file:
                    if '**NODES**' in line:
                        load_nodes = True
                        load_edges = False
                        continue
                    elif '**EDGES**' in line:
                        load_nodes = False
                        load_edges = True
                        continue
                    if load_nodes:
                        if 'children' in line:
                            if 'children' in node_temp:
                                node_temp.append(line.replace('\n', ''))
                                nodes.append(node_temp)
                                node_temp = []
                            else:
                                node_temp.append(line.replace('\n', ''))
                        else:
                            node_temp.append(line.replace('\n', ''))
                    elif load_edges:
                        edge_temp.append(line.replace('\n', ''))
                        if len(edge_temp) == 3:
                            edges.append(edge_temp)
                            edge_temp = []

                parents = False
                children = False
                node_dict = {}
                for node in nodes:
                    self.nodes.append(Node(int(node[2]), int(node[3]), label=node[1], node_id=node[0]))
                    node_dict[node[0]] = self.nodes[-1]
                for node in nodes:
                    for i in range(4, len(node)):
                        if not parents and node[i] == 'parents':
                            parents = True
                            children = False
                            continue
                        elif parents and node[i] == 'parents':
                            parents = False
                        elif parents and node[i] != 'parents':
                            node_dict[node[0]].parents.append(node_dict[node[i]])
                        elif not children and node[i] == 'children':
                            parents = False
                            children = True
                            continue
                        elif children and node[i] != 'children':
                            node_dict[node[0]].children.append(node_dict[node[i]])

                for edge in edges:
                    source = node_dict[edge[0]]
                    target = node_dict[edge[1]]
                    self.edges.append(
                        Edge(source.x, source.y, target.x, target.y, source, target=target, label=edge[2]))
                save_file.close()


class Button:
    def __init__(self, x: int, y: int, label: str, padding=4, border_width=2, border_color=None, border_off=False,
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
    def __init__(self, x_pos, y_pos, label='', text='', padding=4, border_width=2, selected=False, clear_on_init=False):
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


class Label:
    def __init__(self, x: int, y: int, label: str, color=None, font=default_font, font_size=20):
        if color is None:
            color = light_grey
        self.type = 'label'
        self.x = x
        self.y = y
        self.color = color
        self.font = pygame.font.SysFont(font, font_size)
        self.label_text = label
        self.width = int(self.font.render(self.label_text, True, self.color).get_rect().width)
        self.height = int(self.font.render(self.label_text, True, self.color).get_rect().height)

    def draw(self):
        screen.blit(self.font.render(self.label_text, True, self.color), (self.x, self.y))

    def update_pos(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]

    def update_label(self, new_label: str):
        self.label_text = new_label
        self.width = int(self.font.render(self.label_text, True, self.color).get_rect().width)
        self.height = int(self.font.render(self.label_text, True, self.color).get_rect().height)


class Menu:
    def __init__(self, x_pos: int, y_pos: int, source=None, file_name=ran_name):
        self.source = source
        self.x = x_pos
        self.y = y_pos
        self.width = 180
        self.height = screen_height
        self.padding = 7
        self.border_width = 2
        self.items = []
        self.fixtures = []

        # for IDE
        if self.x is None:
            self.source = Node(0, 0)
            self.items.append(Button(0, 0, ''))
            self.items.append(TextBox(0, 0, ''))

        if source is None:
            self.items = [Label(self.x + self.padding, self.y + self.padding, 'No Item Selected')]
            self.items[-1].x = self.x + (self.width / 2) - (self.items[-1].width / 2)

        self.fixtures.append(Button(self.x + self.padding, 0, 'Save', action='save'))
        self.fixtures[-1].y = screen_height - self.fixtures[-1].height - self.padding
        self.fixtures.append(Button(0, 0, 'Load', action='load'))
        self.fixtures[-1].x = self.x + self.width - self.fixtures[-1].width - self.padding
        self.fixtures[-1].y = screen_height - self.fixtures[-1].height - self.padding
        self.fixtures.append(Label(0, 0, 'Or Drag/Drop Tree File', font_size=15))
        self.fixtures[-1].x = self.x + (self.width / 2) - (self.fixtures[-1].width / 2)
        self.fixtures[-1].y = self.fixtures[-2].y - self.padding - self.fixtures[-1].height
        self.fixtures.append(Label(0, 0, 'load.tree', font_size=15, color=blue))
        self.fixtures[-1].x = self.x + (self.width / 2) - (self.fixtures[-1].width / 2)
        self.fixtures[-1].y = self.fixtures[-2].y - self.padding - self.fixtures[-1].height
        self.fixtures.append(Label(0, 0, 'To load, name file as:', font_size=15))
        self.fixtures[-1].x = self.x + (self.width / 2) - (self.fixtures[-1].width / 2)
        self.fixtures[-1].y = self.fixtures[-2].y - self.padding - self.fixtures[-1].height
        self.fixtures.append(Label(0, 0, file_name + '.tree', font_size=15, color=blue))
        self.fixtures[-1].x = self.x + (self.width / 2) - (self.fixtures[-1].width / 2)
        self.fixtures[-1].y = self.fixtures[-2].y - self.padding - self.fixtures[-1].height
        self.fixtures.append(Label(0, 0, 'Save will save file as:', font_size=15))
        self.fixtures[-1].x = self.x + (self.width / 2) - (self.fixtures[-1].width / 2)
        self.fixtures[-1].y = self.fixtures[-2].y - self.padding - self.fixtures[-1].height

        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(dark_grey)
        self.background.set_alpha(230)

    def draw(self):
        tree.menu.refresh_data()
        # pygame.draw.rect(screen, dark_grey, (self.x, self.y, self.width, self.height))
        screen.blit(self.background, (self.x, self.y))

        for item in self.items:
            item.draw()

        for fixture in self.fixtures:
            fixture.draw()

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
                y_offset = 0
                if source.type == 'node':
                    self.items = [Label(self.x + self.padding, self.y + self.padding, 'Selected Node:')]
                    self.items[-1].x = self.x + (self.width / 2) - (self.items[-1].width / 2)
                    y_offset += self.items[-1].height + self.padding
                    self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                              label='Label', text=''))
                    y_offset += self.items[-1].height + self.padding
                    self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                              label='Children', text=''))

                    for item in self.items:
                        if item.type == 'textbox':
                            if item.x + item.width + item.label_offset != self.width - self.padding * 2:
                                item.width += self.width - self.padding * 2 - item.width - item.label_offset
                                item.min_width = item.width

                elif source.type == 'edge':
                    self.items = [Label(self.x + self.padding, self.y + self.padding, 'Selected Edge:')]
                    self.items[-1].x = self.x + (self.width / 2) - (self.items[-1].width / 2)
                    y_offset += self.items[-1].height + self.padding
                    self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                              label='Label', text=source.label))

                    for item in self.items:
                        if item.type == 'textbox':
                            if item.x + item.width + item.label_offset != self.width - self.padding * 2:
                                item.width += self.width - self.padding * 2 - item.width - item.label_offset
                                item.min_width = item.width
            else:
                self.source.sourced = False
                y_offset = 0
                if source.type == self.source.type:
                    self.refresh_data()

                elif source.type == 'node':
                    self.items = [Label(self.x + self.padding, self.y + self.padding, 'Selected Node:')]
                    self.items[-1].x = self.x + (self.width / 2) - (self.items[-1].width / 2)
                    y_offset += self.items[-1].height + self.padding
                    self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                              label='Label', text=''))
                    y_offset += self.items[-1].height + self.padding
                    self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                              label='Children', text=''))

                    for item in self.items:
                        if item.type == 'textbox':
                            if item.x + item.width + item.label_offset != self.width - self.padding * 2:
                                item.width += self.width - self.padding * 2 - item.width - item.label_offset
                                item.min_width = item.width

                elif source.type == 'edge':
                    self.items = [Label(self.x + self.padding, self.y + self.padding, 'Selected Edge:')]
                    self.items[-1].x = self.x + (self.width / 2) - (self.items[-1].width / 2)
                    y_offset += self.items[-1].height + self.padding
                    self.items.append(TextBox(self.x + self.padding, self.y + y_offset + self.padding,
                                              label='Label', text=source.label))

                    for item in self.items:
                        if item.type == 'textbox':
                            if item.x + item.width + item.label_offset != self.width - self.padding * 2:
                                item.width += self.width - self.padding * 2 - item.width - item.label_offset
                                item.min_width = item.width

            self.source = source
            self.source.sourced = True

            # Select Label textbox
            for item in self.items:
                if item.type == 'textbox' and item.label == 'Label':
                    item.selected = True
        else:
            self.source = None
            self.items = [Label(self.x + self.padding, self.y + self.padding, 'No Item Selected')]
            self.items[-1].x = self.x + (self.width / 2) - (self.items[-1].width / 2)

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

    def resize(self):
        self.height = screen_height
        self.fixtures[0].y = screen_height - self.fixtures[0].height - self.padding
        self.fixtures[1].y = screen_height - self.fixtures[1].height - self.padding
        for i in range(len(self.fixtures)):
            if self.fixtures[i].type == 'label':
                self.fixtures[i].x = self.x + (self.width / 2) - (self.fixtures[i].width / 2)
                self.fixtures[i].y = self.fixtures[i - 1].y - self.padding - self.fixtures[i].height

        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(dark_grey)
        self.background.set_alpha(230)


class SelectionBox:
    def __init__(self, x_pos: int, y_pos: int, width=2, color=None):
        self.selected = False
        self.selection = []
        self.held = False
        self.held_offset = [0, 0]
        self.x = x_pos
        self.y = y_pos
        self.end_x = self.x
        self.end_y = self.y
        if color is None:
            color = white
        self.color = color
        self.width = width
        self.x_range = (self.x, self.x)
        self.y_range = (self.y, self.y)

    def draw(self, offset=(0, 0)):
        pygame.draw.rect(screen, self.color, (self.x - offset[0], self.y - offset[1],
                                              self.end_x - self.x, self.end_y - self.y),
                         width=self.width)

    def update_end_pos(self, pos: tuple):
        self.end_x = pos[0]
        self.end_y = pos[1]

        self.update_range()

    def update_pos(self, pos: tuple):
        offset = ((pos[0] + self.held_offset[0]) - self.x, (pos[1] + self.held_offset[1]) - self.y)

        if len(self.selection) > 0:
            for node in self.selection:
                node.x += offset[0]
                node.y += offset[1]

        self.x += offset[0]
        self.end_x += offset[0]
        self.y += offset[1]
        self.end_y += offset[1]

        self.update_range()

    def make_selection(self, selected=True, selected_object=None, hold_offset=(0, 0)):
        self.selected = selected
        if selected_object is not None:
            for node in selected_object:
                node.held_offset = [node.x - hold_offset[0], node.y - hold_offset[1]]
                node.selected = True
                self.selection.append(node)

    def resize_box(self):
        x_range = [screen_width, 0]
        y_range = [screen_height, 0]
        if len(self.selection) > 0:
            for node in self.selection:
                if node.x - node.radius < x_range[0]:
                    x_range[0] = node.x - node.radius
                if node.x + node.radius > x_range[1]:
                    x_range[1] = node.x + node.radius
                if node.y - node.radius < y_range[0]:
                    y_range[0] = node.y - node.radius
                if node.y + node.radius > y_range[1]:
                    y_range[1] = node.y + node.radius
        self.x = x_range[0] - self.width * 2
        self.end_x = x_range[1] + self.width * 2
        self.y = y_range[0] - self.width * 2
        self.end_y = y_range[1] + self.width * 2
        self.update_range()

    def update_range(self):
        if self.x <= self.end_x:
            self.x_range = (self.x, self.end_x)
        elif self.x >= self.end_x:
            self.x_range = (self.end_x, self.x)

        if self.y <= self.end_y:
            self.y_range = (self.y, self.end_y)
        elif self.y >= self.end_y:
            self.y_range = (self.end_y, self.y)


# Undo function, Zoom function (deceptively hard), auto-sort feature, color palette choices
# Fix menu generally, textbox scrolling. Tab to select children, shift tab to jump to parent
# Save/load to file, reorganize everything, add copy paste, ability to move textbox cursor


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
    global box_select
    global allow_box_select

    def create_new_node(held=True, update_menu=True):
        global auto_name
        global draw_edge

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

        for node__ in tree.nodes:
            if auto_name == node__.label:
                create_new_node()
                return

        # Why do I need to do this draw_edge check??
        if not draw_edge:
            tree.nodes.append(Node(mouse_pos[0] - tree.view_offset[0], mouse_pos[1] - tree.view_offset[1],
                                   held=held, label=auto_name))
        else:
            tree.nodes.append(Node(mouse_pos[0], mouse_pos[1], held=held, label=auto_name))

        if update_menu:
            tree.menu.update_source(tree.nodes[-1])

        if draw_edge:
            edge__ = tree.edges[-1]
            draw_edge = False
            edge__.parent.draw_edge = False
            edge__.held = False
            edge__.child = tree.nodes[-1]
            edge__.update_pos()
            if edge__.label == '':
                edge__.label = edge__.parent.label + '>' + edge__.child.label
            # Update nodes data
            edge__.parent.children.append(edge__.child)
            edge__.child.parents.append(edge__.parent)

    if event_type == 'down':
        # Left click
        if mouse_buttons[0]:
            left_mouse_held = True

            menu_item_click = False
            for item in tree.menu.items:
                if item.type == 'button':
                    if item.check_collide(mouse_pos):
                        menu_item_click = True
                    item.mouse_input(mouse_pos, mouse_buttons, 'down')
            for fixture in tree.menu.fixtures:
                if fixture.type == 'button':
                    if fixture.check_collide(mouse_pos):
                        menu_item_click = True
                    fixture.mouse_input(mouse_pos, mouse_buttons, 'down')

            if mouse_pos[0] > tree.menu.width:
                # Left click in selection box
                if not allow_box_select and tree.selection_box is not None and tree.selection_box.selected and \
                        tree.selection_box.x_range[0] <= mouse_pos[0] <= tree.selection_box.x_range[1] and \
                        tree.selection_box.y_range[0] <= mouse_pos[1] <= tree.selection_box.y_range[1]:
                    tree.selection_box.held = True
                    tree.selection_box.held_offset = (tree.selection_box.x - mouse_pos[0],
                                                      tree.selection_box.y - mouse_pos[1])
                else:
                    node_click = False
                    # Left click node
                    for node in tree.nodes:
                        if ((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2)**0.5 <= node.radius + 1:
                            if not draw_edge:
                                node_click = True
                                node.held_offset = [node.x - mouse_pos[0], node.y - mouse_pos[1]]
                                node.held = True
                                tree.menu.update_source(node)

                    # Left click background
                    if not node_click:
                        if not allow_box_select:
                            view_drag = True

                            rename_this_later = True
                            # Double click to create new node
                            if double_click and double_click_timer > 0:
                                if not box_select:
                                    create_new_node()
                                    double_click_timer = 0
                                    double_click = False
                                    view_drag = False
                                    rename_this_later = False
                                else:
                                    box_select = False

                            if rename_this_later:
                                if view_drag:
                                    view_drag_temp = tree.view_offset
                                    orig_mouse_pos = mouse_pos

                                # Select Edge
                                edge_click = False
                                for edge in tree.edges:
                                    if edge.check_collide(mouse_pos):
                                        tree.menu.update_source(edge)
                                        edge_click = True

                                # Select menu item
                                if not edge_click:
                                    for item in tree.menu.items:
                                        if item.type == 'textbox':
                                            item.blink_counter = 0
                                            item.selected = False
                                            if item.check_collide(mouse_pos):
                                                item.selected = True
                        elif allow_box_select and not box_select:
                            box_select = True
                            if tree.selection_box is None:
                                tree.selection_box = SelectionBox(mouse_pos[0], mouse_pos[1])
                        elif allow_box_select and box_select and tree.selection_box is not None:
                            tree.selection_box = None
                            tree.selection_box = SelectionBox(mouse_pos[0], mouse_pos[1])

                    if not double_click:
                        double_click = True
                        double_click_timer = int(frame_rate / 3)
            elif not menu_item_click:
                for item in tree.menu.items:
                    if item.type == 'textbox':
                        item.selected = False

        # Right click
        if mouse_buttons[2]:
            right_mouse_held = True
            if mouse_pos[0] > tree.menu.width:
                node_click = False
                # Right click node
                for node in tree.nodes:
                    if ((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2)**0.5 <= node.radius + 1:
                        node_click = True
                        if not draw_edge:
                            if not node.draw_edge:
                                node.draw_edge = True
                            else:
                                node.draw_edge = False
                            break
                # Right click background
                if not node_click:
                    if draw_edge:
                        create_new_node(held=False, update_menu=False)
    elif event_type == 'up':
        # Left unclick
        if not mouse_buttons[0]:
            if left_mouse_held:
                view_drag = False
                for item in tree.menu.items:
                    if item.type == 'button':
                        item.mouse_input(mouse_pos, mouse_buttons, 'up')
                    elif item.type == 'textbox' and item.label != 'Children' and item.check_collide(mouse_pos):
                        item.selected = True
                for fixture in tree.menu.fixtures:
                    if fixture.type == 'button':
                        fixture.mouse_input(mouse_pos, mouse_buttons, 'up')

                if tree.selection_box is not None and \
                        view_drag_temp == (0, 0) and len(tree.selection_box.selection) > 0:
                    if tree.selection_box.x_range[0] <= mouse_pos[0] <= tree.selection_box.x_range[1] and \
                            tree.selection_box.y_range[0] <= mouse_pos[1] <= tree.selection_box.y_range[1]:
                        # Left unclick node
                        node_click = False
                        for node in tree.nodes:
                            if ((node.x - mouse_pos[0]) ** 2 + (node.y - mouse_pos[1]) ** 2) ** 0.5 <= node.radius + 1:
                                tree.menu.update_source(node)
                                node_click = True
                                break
                        if not node_click:
                            for edge in tree.edges:
                                if edge.check_collide(mouse_pos):
                                    tree.menu.update_source(edge)
                                    break
                    else:
                        for node in tree.selection_box.selection:
                            node.selected = False
                        tree.selection_box = None
                        box_select = False

                tree.view_offset = (tree.view_offset[0] + view_drag_temp[0], tree.view_offset[1] + view_drag_temp[1])
                # Update node pos from view drag
                for node in tree.nodes:
                    node.x -= view_drag_temp[0]
                    node.y -= view_drag_temp[1]
                for edge in tree.edges:
                    edge.update_pos()
                if tree.selection_box is not None and tree.selection_box.selected:
                    tree.selection_box.held = False
                    tree.selection_box.x -= view_drag_temp[0]
                    tree.selection_box.end_x -= view_drag_temp[0]
                    tree.selection_box.y -= view_drag_temp[1]
                    tree.selection_box.end_y -= view_drag_temp[1]
                    tree.selection_box.update_range()
                view_drag_temp = (0, 0)

                # Select nodes with box
                if tree.selection_box is not None and not tree.selection_box.selected:
                    selection = []
                    for node in tree.nodes:
                        if tree.selection_box.x_range[0] <= node.x + node.radius and \
                                node.x - node.radius <= tree.selection_box.x_range[1]:
                            if tree.selection_box.y_range[0] <= node.y + node.radius and \
                                    node.y - node.radius <= tree.selection_box.y_range[1]:
                                selection.append(node)
                            elif node is not tree.menu.source:
                                node.selected = False
                                node.held = False
                        elif node is not tree.menu.source:
                            node.selected = False
                            node.held = False
                    if len(selection) > 1:
                        tree.selection_box.make_selection(selected_object=selection, hold_offset=mouse_pos)
                    if len(tree.selection_box.selection) == 0:
                        tree.selection_box = None
                        box_select = False
                    else:
                        tree.selection_box.resize_box()
                else:
                    for node in tree.nodes:
                        node.held = False

            left_mouse_held = False

        # Right unclick
        if not mouse_buttons[2]:
            if right_mouse_held:
                if mouse_pos[0] > tree.menu.width:
                    for node in tree.nodes:
                        if ((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2)**0.5 <= node.radius + 1:
                            if draw_edge and not node.draw_edge:
                                edge = tree.edges[-1]
                                if node not in edge.parent.children and edge.parent is not node:
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
                                    break

            right_mouse_held = False

    # Button actions
    for item in tree.menu.items:
        if item.type == 'button':
            if item.run:
                if item.action == 'node':
                    create_new_node()
                item.run = False
            else:
                item.mouse_input(mouse_pos, mouse_buttons, '')
    for fixture in tree.menu.fixtures:
        if fixture.type == 'button':
            if fixture.run:
                if fixture.action == 'save':
                    tree.save_tree()
                    fixture.run = False
                    fixture.pressed = False
                    fixture.pressed_draw = False
                elif fixture.action == 'load':
                    tree.load_tree()
                    fixture.run = False
                    fixture.pressed = False
                    fixture.pressed_draw = False
            else:
                fixture.mouse_input(mouse_pos, mouse_buttons, '')

    # Nodes / Edges
    for node in tree.nodes:
        if node.held:
            node.update_pos(mouse_pos)
        elif node.draw_edge:
            if not draw_edge:
                distance_to_node = ((node.x - mouse_pos[0]) ** 2 + (node.y - mouse_pos[1]) ** 2) ** 0.5
                if abs(distance_to_node) >= node.radius + 5:
                    tree.edges.append(Edge(node.x - tree.view_offset[0], node.y - tree.view_offset[1], 0, 0, node))
                    draw_edge = True
            else:
                distance_to_node = ((node.x - mouse_pos[0]) ** 2 + (node.y - mouse_pos[1]) ** 2) ** 0.5
                if abs(distance_to_node) <= node.radius + 1:
                    draw_edge = False
                    tree.edges.pop()
    if draw_edge and not view_drag:
        tree.edges[-1].update_pos(mouse_pos)

    # View drag
    if view_drag:
        view_drag_temp = (orig_mouse_pos[0] - mouse_pos[0], orig_mouse_pos[1] - mouse_pos[1])

    # Box select
    if tree.selection_box is not None:
        if not tree.selection_box.selected:
            tree.selection_box.update_end_pos(mouse_pos)
        elif tree.selection_box.held:
            tree.selection_box.update_pos(mouse_pos)


def bullshit_fix():
    if loaded_file == '' and ran_name not in tree.menu.fixtures[5].label_text:
        tree.menu.fixtures[5].update_label(ran_name + '.tree')
        tree.menu.resize()
    elif loaded_name != '' and loaded_name not in tree.menu.fixtures[5].label_text:
        tree.menu.fixtures[5].update_label(loaded_name + '.tree')
        tree.menu.resize()


def delete_object(deleted_object=None, undo=False):
    global deleted_objects
    global tree

    if not undo and deleted_object is not None:
        deleted_object.deleted = True
        deleted_object.sourced = False
        deleted_object.selected = False
        deleted_object.held = False
        deleted_objects.append(deleted_object)

        if deleted_object.type == 'node':
            if len(deleted_object.parents) != 0 or len(deleted_object.children) != 0:
                pop_list = []
                for edge_ in reversed(tree.edges):
                    if edge_.parent == deleted_object or edge_.child == deleted_object:
                        pop_list.append(tree.edges.index(edge_))
                for index_ in pop_list:
                    delete_object(deleted_object=tree.edges[index_])
            tree.nodes.pop(tree.nodes.index(deleted_object))
        elif deleted_object.type == 'edge':
            # For IDE
            if delete_timer < 0:
                edge_ = Edge(0, 0, 0, 0, None)
            else:
                edge_ = deleted_object

            edge_.parent.children.pop(edge_.parent.children.index(edge_.child))
            edge_.child.parents.pop(edge_.child.parents.index(edge_.parent))
            tree.edges.pop(tree.edges.index(deleted_object))

        if tree.menu.source is not None and tree.menu.source == deleted_object:
            tree.menu.update_source(None)
    elif undo and len(deleted_objects) > 0:
        edges_to_restore = []
        for i in reversed(range(len(deleted_objects))):
            if deleted_objects[i].type == 'edge':
                edges_to_restore.append(deleted_objects[i])
            elif deleted_objects[i].type == 'node':
                deleted_objects[i].deleted = False
                tree.nodes.append(deleted_objects[i])
                deleted_objects.pop(deleted_objects.index(deleted_objects[i]))
                if len(edges_to_restore) > 0:
                    for edge_ in edges_to_restore:
                        edge_.deleted = False
                        edge_.parent.children.append(edge_.child)
                        edge_.child.parents.append(edge_.parent)
                        tree.edges.append(edge_)
                        deleted_objects.pop(deleted_objects.index(edge_))
                break


tree = Tree()
deleted_objects = []

# Maybe label these
loaded_file = ''
loaded_name = ''
delete_item = False
delete_timer = 0
left_mouse_held = False
double_click = False
auto_name = ''
double_click_timer = 0
right_mouse_held = False
view_drag = False
allow_box_select = False
box_select = False
orig_mouse_pos = (0, 0)
view_drag_temp = (0, 0)
draw_edge = False
held_key = ''
held_key_event = None
key_hold_counter = 0
running = True
while running:

    # Event loop
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        # Close window
        if event.type == QUIT:
            running = False
            break

        # Key down events
        elif event.type == KEYDOWN:
            # Ctrl functions
            if keys[K_LCTRL] or keys[K_RCTRL]:
                allow_box_select = True

                # Save tree
                if keys[K_s]:
                    tree.save_tree()

                # Close window shortcut
                elif keys[K_w]:
                    running = False
                    break

                # Return to original view position
                elif keys[K_o]:
                    for node_ in tree.nodes:
                        node_.x += tree.view_offset[0]
                        node_.y += tree.view_offset[1]
                    tree.view_offset = (0, 0)

                elif keys[K_z]:
                    delete_object(undo=True)

            # Delete selected item
            elif keys[K_DELETE]:
                if not delete_item:
                    delete_item = True
                    delete_timer = int(frame_rate / 2)
                elif delete_timer > 0:
                    if tree.menu.source is not None:
                        delete_object(tree.menu.source)
                    delete_item = False

            else:
                # Send input to Menu textbox
                for item_ in tree.menu.items:
                    if item_.type == 'textbox':
                        if tree.menu.source is not None and item_.selected:
                            if keys[K_BACKSPACE]:
                                held_key = 'backspace'
                                key_hold_counter = int(frame_rate)
                                item_.update_text(backspace=True)
                            elif item_.label == 'Children':
                                if event.unicode in integers:
                                    held_key = event.unicode
                                    held_key_event = event
                                    key_hold_counter = int(frame_rate)
                                    item_.update_text(event.unicode)
                            else:
                                held_key = event.unicode
                                held_key_event = event
                                key_hold_counter = int(frame_rate)
                                item_.update_text(event.unicode)

                            # update node data
                            if item_.label == 'Label':
                                tree.menu.source.label = item_.text

        # Key up events
        elif event.type == KEYUP:
            if not keys[K_LCTRL] and not keys[K_RCTRL]:
                allow_box_select = False
            if held_key != '':
                if held_key == 'backspace' and not keys[K_BACKSPACE]:
                    held_key = ''
                elif held_key_event is not None:
                    if held_key == held_key_event.unicode and event not in keys:
                        held_key = ''
                        held_key_event = None

        # Mouse down event
        elif event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                mouse_handler('down', pygame.mouse.get_pos(), pygame.mouse.get_pressed())

        # Mouse up event
        elif event.type == MOUSEBUTTONUP:
            if left_mouse_held or right_mouse_held:
                mouse_handler('up', pygame.mouse.get_pos(), pygame.mouse.get_pressed())

        # Mousewheel
        elif event.type == MOUSEWHEEL:
            if not event.flipped:
                pass
            else:
                pass

        # Resize
        elif event.type == VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
            tree.menu.resize()

        # Load file
        elif event.type == DROPFILE:
            tree.load_tree(from_file=True, file_path=event.file)

    mouse_handler('', pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    # Timers
    if held_key != '' and key_hold_counter == 0:
        key_hold_counter = int(frame_rate / 30)
        for item_ in tree.menu.items:
            if item_.type == 'textbox':
                if item_.selected:
                    if held_key == 'backspace':
                        item_.update_text(backspace=True)
                    else:
                        item_.update_text(held_key)
                # Update source object
                    if item_.label == 'Label':
                        tree.menu.source.label = item_.text
                    break
    elif key_hold_counter > 0:
        key_hold_counter -= 1

    # Double press to delete timer
    if delete_item and delete_timer > 0:
        delete_timer -= 1
        if delete_timer == 0:
            delete_item = False

    # Double click timer
    if double_click and double_click_timer > 0:
        double_click_timer -= 1
        if double_click_timer == 0:
            double_click = False

    bullshit_fix()
    tree.draw_screen()

    clock.tick(frame_rate)
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
