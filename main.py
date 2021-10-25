import math
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
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 200, 255]
light_grey = [200, 200, 200]
dark_grey = [75, 75, 75]
grey = [128, 128, 128]

bg_color = dark_grey
# Font
default_font = 'Georgia'

integers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


class Node:
    def __init__(self, x_pos: int, y_pos: int, label='', parents=None, children=None, radius=10,
                 font=default_font, font_size=20, held=False):
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
        if self.held:
            self.x = pos[0] + self.held_offset[0]
            self.y = pos[1] + self.held_offset[1]
        else:
            self.x = pos[0]
            self.y = pos[1]

    def draw(self):
        if self.selected:
            pygame.draw.circle(screen, red, (self.x, self.y), self.radius)
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius - 2)
        else:
            pygame.draw.circle(screen, black, (self.x, self.y), self.radius)
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius - 2)
        if self.show_label:
            label = self.font.render(self.label, True, self.color)
            label_x = int(label.get_rect().width / 2)
            screen.blit(label, (self.x - label_x, self.y - self.radius - 25))


class Edge:
    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int, width: int, source: object, target=None,
                 held=False, label='', font=default_font, font_size=20):
        self.label = label
        self.show_label = False
        self.font = font
        self.font_size = font_size
        self.x = start_x
        self.y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.width = width
        self.held = held
        self.selected = False
        self.source = source
        self.target = target
        self.type = 'edge'

        # for IDE
        if self.x is None:
            self.source = Node(0, 0)
            self.target = Node(0, 0)

    def draw(self):
        pygame.draw.line(screen, black, (self.x, self.y), (self.end_x, self.end_y), self.width)
        p = (0.4, 0.6)
        middle = (int(p[0] * self.x + p[1] * self.end_x), int(p[0] * self.y + p[1] * self.end_y))
        rotation = math.degrees(math.atan2(self.y - self.end_y, self.end_x - self.x)) + 90
        plus = 165
        times = 20
        pygame.draw.polygon(screen, black, (middle,
                                            (int(middle[0] + times * math.sin(math.radians(rotation - plus))),
                                             int(middle[1] + times * math.cos(math.radians(rotation - plus)))),
                                            (int(middle[0] + times * math.sin(math.radians(rotation + plus))),
                                             int(middle[1] + times * math.cos(math.radians(rotation + plus))))))

    def update_pos(self, pos=None):
        if pos is None:
            if self.source is not None:
                self.x = self.source.x
                self.y = self.source.y
            if self.target is not None:
                self.end_x = self.target.x
                self.end_y = self.target.y
        else:
            self.end_x = pos[0]
            self.end_y = pos[1]


class Tree:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.menu = Menu(0, 0)

    def draw_screen(self):
        for edge in self.edges:
            edge.update_pos()
            edge.draw()
        for node in self.nodes:
            node.draw()

        self.menu.draw()


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
        # Background
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.width + self.label_offset, self.height))

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

        x_offset = 0
        y_offset = 45
        width = 0
        if source is None:
            self.items = [Button(self.x + x_offset + self.padding, self.y + self.padding,
                                 'Create New Node', action='node')]
            width = self.items[0].width + self.padding
            self.items.append(TextBox(self.x + x_offset + self.padding, self.y + y_offset + self.padding,
                                      label='Label', text=''))
            self.items[1].min_width *= 2
            self.items[1].width *= 2
            y_offset += self.items[0].height + self.padding
            self.items.append(TextBox(self.x + x_offset + self.padding, self.y + y_offset + self.padding,
                                      label='Children', text=''))
            self.items[1].min_width *= 2
            self.items[1].width *= 2
            y_offset += self.items[1].height + self.padding
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

        if self.source is None:
            self.source = source
        else:
            self.source.selected = False
            self.source = source

        for item in self.items:
            if item.type == 'textbox':
                if item.label == 'Label':
                    item.clear_text()
                    item.update_text(source.label)
                elif item.label == 'Children':
                    item.clear_text()
                    item.update_text(str(len(source.children)))

        source.selected = True

    def refresh_data(self):
        if self.source is not None:
            for item in self.items:
                if item.type == 'textbox':
                    if item.label == 'Label':
                        if self.source.label != item.text:
                            item.clear_text()
                            item.update_text(self.source.label)
                    elif item.label == 'Children':
                        if str(len(self.source.children)) != item.text:
                            item.clear_text()
                            item.update_text(str(len(self.source.children)))


# Don't allow duplicate edges, right click empty space with edge creates new node, allow removal of edges and nodes,
# Auto name new nodes, Fix menu, textbox scrolling, box select, edges show label


def mouse_handler(event_type: str, mouse_pos: tuple, mouse_buttons: tuple):
    global left_mouse_held
    global right_mouse_held
    global tree
    global draw_edge

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
                # Select menu item
                for item in tree.menu.items:
                    item.blink_counter = 0
                    item.selected = False
                    if item.check_collide(mouse_pos):
                        item.selected = True

        # Right click
        if mouse_buttons[2]:
            right_mouse_held = True
            node_click = False
            # Right click node
            for node in tree.nodes:
                if ((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2)**0.5 <= node.radius + 1:
                    node_click = True
                    node.draw_edge = True
                    break
            # Right click background
            if not node_click:
                pass
    elif event_type == 'up':
        for item in tree.menu.items:
            if item.type == 'button':
                item.mouse_input(mouse_pos, mouse_buttons, 'up')
        # Left unclick
        if not mouse_buttons[0]:
            left_mouse_held = False
            for node in tree.nodes:
                node.held = False
        # Right unclick
        if not mouse_buttons[2]:
            right_mouse_held = False
            for node in tree.nodes:
                if ((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2)**0.5 <= node.radius + 1:
                    if draw_edge:
                        draw_edge = False
                        edge = tree.edges[-1]
                        edge.source.draw_edge = False
                        edge.held = False
                        edge.target = node
                        edge.update_pos()
                        # Update nodes data
                        edge.source.children.append(edge.target)
                        edge.target.parents.append(edge.source)

                    # Open Node data menu
                    elif node.draw_edge:
                        node.draw_edge = False
                    break

    # Button actions
    for item in tree.menu.items:
        if item.type == 'button':
            if item.run:
                if item.action == 'node':
                    highest_letter = -1
                    node_name = 'A'
                    for node in tree.nodes:
                        if len(node.label) == 1:
                            for i in range(len(capital_letters)):
                                if node.label[0] == capital_letters[i]:
                                    if i > highest_letter:
                                        highest_letter = i
                    not_in_set = []
                    for i in range(0, highest_letter):
                        letter_not_in_set = True
                        for node in tree.nodes:
                            if len(node.label) == 1 and node.label[0] == capital_letters[i]:
                                letter_not_in_set = False
                                break
                        if letter_not_in_set:
                            not_in_set.append(i)

                    if len(not_in_set) == 0:
                        if -1 <= highest_letter < 25:
                            node_name = capital_letters[highest_letter + 1]
                        # Repeat for second character
                        else:
                            highest_letter = -1
                            for node in tree.nodes:
                                if len(node.label) == 2:
                                    for i in range(len(capital_letters)):
                                        if node.label[1] == capital_letters[i]:
                                            if i > highest_letter:
                                                highest_letter = i
                            not_in_set = []
                            for i in range(0, highest_letter):
                                letter_not_in_set = True
                                for node in tree.nodes:
                                    if len(node.label) == 2 and node.label[1] == capital_letters[i]:
                                        letter_not_in_set = False
                                        break
                                if letter_not_in_set:
                                    not_in_set.append(i)

                            if len(not_in_set) == 0:
                                if -1 <= highest_letter < 25:
                                    node_name += capital_letters[highest_letter + 1]
                                else:
                                    node_name += 'A#'
                            else:
                                node_name = capital_letters[not_in_set[0]]
                    else:
                        node_name = capital_letters[not_in_set[0]]

                    tree.nodes.append(Node(mouse_pos[0], mouse_pos[1], held=True, label=node_name))
                    tree.menu.update_source(tree.nodes[-1])
                item.run = False
            else:
                item.mouse_input(mouse_pos, mouse_buttons, '')

    # Nodes / Edges
    for node in tree.nodes:
        if node.held:
            node.update_pos(mouse_pos)
        elif not draw_edge and node.draw_edge:
            if abs(distance_to_node) >= node.radius + 5:
                tree.edges.append(Edge(node.x, node.y, 0, 0, 3, node))
                draw_edge = True
        elif node.draw_edge:
            if abs(distance_to_node) <= node.radius + 1:
                draw_edge = False
                tree.edges.pop()
    if draw_edge:
        tree.edges[-1].update_pos(mouse_pos)


def debug_(variables: list):
    global debug

    if debug != variables:
        debug = variables
        print(debug)


tree = Tree()

left_mouse_held = False
right_mouse_held = False
draw_edge = False
held_key = ''
held_key_event = None
key_hold_counter = 0
running = True
while running:
    screen.fill(bg_color)
    tree.draw_screen()

    # Event loop
    for event in pygame.event.get():
        # Close window
        if event.type == pygame.QUIT:
            running = False
            break

        # Key down events
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            # Close window shortcut
            if (keys[K_LCTRL] or keys[K_RCTRL]) and keys[K_w]:
                running = False
                break

            # Send input to Menu textbox
            for m_item in tree.menu.items:
                if m_item.type == 'textbox':
                    if tree.menu.source is not None and m_item.selected:
                        if keys[K_BACKSPACE]:
                            held_key = 'backspace'
                            key_hold_counter = frame_rate
                            m_item.update_text(backspace=True)
                        elif m_item.label == 'Children':
                            if event.unicode in integers:
                                held_key = event.unicode
                                held_key_event = event
                                key_hold_counter = frame_rate
                                m_item.update_text(event.unicode)
                        else:
                            held_key = event.unicode
                            held_key_event = event
                            key_hold_counter = frame_rate
                            m_item.update_text(event.unicode)

                        # update node data
                        if m_item.label == 'Label':
                            tree.menu.source.label = m_item.text
                        elif m_item.label == 'Children':
                            pass

        # Key up events
        if event.type == pygame.KEYUP:
            if held_key != '':
                if held_key == 'backspace' and not keys[K_BACKSPACE]:
                    held_key = ''
                elif held_key_event is not None:
                    if held_key == held_key_event.unicode and event not in keys:
                        held_key = ''
                        held_key_event = None

        # Mouse down event
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_handler('down', pygame.mouse.get_pos(), pygame.mouse.get_pressed())

        # Mouse up event
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_handler('up', pygame.mouse.get_pos(), pygame.mouse.get_pressed())

        # Resize
        if event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
            tree.menu.height = screen_height

    mouse_handler('', pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    if held_key != '' and key_hold_counter == 0:
        key_hold_counter = frame_rate / 30
        for m_item in tree.menu.items:
            if m_item.selected:
                if held_key == 'backspace':
                    m_item.update_text(backspace=True)
                else:
                    m_item.update_text(held_key)
                break
    elif key_hold_counter > 0:
        key_hold_counter -= 1

    clock.tick(frame_rate)
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
