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
screen = pygame.display.set_mode((screen_width, screen_height))
# Title
pygame.display.set_caption('Decision Tree Tool')
# Colors
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [10, 90, 255]
grey = gray = [128, 128, 128]
grid_color = [50, 50, 50]
# Font
default_font = 'Helvetica'

integers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


class Node:
    def __init__(self, x_pos: int, y_pos: int, label: str, level: int, parents=None, children=None, radius=10,
                 font=default_font, font_size=20, held=False):
        self.x = x_pos
        self.y = y_pos
        self.radius = radius
        self.label = label
        self.level = level
        self.color = blue
        self.font = pygame.font.SysFont(font, font_size)
        self.show_label = True
        self.held = held
        self.held_offset = [0, 0]
        self.draw_edge = False
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
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
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
        self.source = source
        self.target = target

        # for IDE
        if self.x is None:
            self.source = Node(0, 0, '', 0)
            self.target = Node(0, 0, '', 0)

    def draw(self):
        global debug

        pygame.draw.line(screen, grey, (self.x, self.y), (self.end_x, self.end_y), self.width)
        p = (0.4, 0.6)
        middle = (int(p[0] * self.x + p[1] * self.end_x), int(p[0] * self.y + p[1] * self.end_y))
        rotation = math.degrees(math.atan2(self.y - self.end_y, self.end_x - self.x)) + 90
        plus = 155
        times = 20
        pygame.draw.polygon(screen, grey, (middle,
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

    def draw_tree(self):
        for edge in self.edges:
            edge.update_pos()
            edge.draw()
        for node in self.nodes:
            node.draw()


class Button:
    def __init__(self, x: int, y: int, label: str, padding=5, border_width=2, border_color=None, border_off=False,
                 button_color=None, font=default_font, font_size=20, font_color=None, action=None, highlight=False):
        if action is None:
            self.action = ''
        else:
            self.action = action
        if border_color is None:
            border_color = white
        if font_color is None:
            font_color = white
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
        self.color = white
        self.bg_color = black
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
    def __init__(self, x_pos: int, y_pos: int, source_str: str, source: object):
        self.source = source
        self.source_offset = (7, 0)
        self.x = x_pos + self.source_offset[0]
        self.y = y_pos + self.source_offset[1]
        self.padding = 7
        self.border_width = 2
        self.items = []

        # for IDE
        if self.x is None:
            self.source = Node(0, 0, '', 0)

        x_offset = 0
        y_offset = 25
        width = 0
        if source_str == 'node':
            self.items = [(TextBox(self.x + x_offset + self.padding, self.y + y_offset + self.padding,
                                   label='Label', text=self.source.label))]
            self.items[0].min_width *= 2
            self.items[0].width *= 2
            y_offset += self.items[0].height + 3
            self.items.append(TextBox(self.x + x_offset + self.padding, self.y + y_offset + self.padding,
                                      label='Children', text=str(len(self.source.children))))
            self.items[1].min_width *= 2
            self.items[1].width *= 2
            y_offset += self.items[1].height + 3
            for item in self.items:
                if item.width + item.label_offset > width:
                    width = item.width + item.label_offset
        self.width = width + self.padding * 2
        self.height = y_offset + self.padding * 2 - 3
        for item in self.items:
            if item.x + item.width + item.label_offset != width:
                item.width += width - item.width - item.label_offset
                item.min_width = item.width

        self.close_button = Button(self.x + self.width - self.padding - 20, self.y + self.padding - 10,
                                   label='x', border_off=True)
        self.update_pos()

    def draw(self):
        for item in self.items:
            item.draw()

        self.close_button.draw()

        # Left edge
        pygame.draw.rect(screen, white, (self.x, self.y, self.border_width, self.height))
        # Top edge
        pygame.draw.rect(screen, white, (self.x, self.y, self.width, self.border_width))
        # Bottom edge
        pygame.draw.rect(screen, white, (self.x, self.y + self.height - self.border_width, self.width,
                                         self.border_width))
        # Right edge
        pygame.draw.rect(screen, white, (self.x + self.width - self.border_width,
                                         self.y, self.border_width, self.height))

    def update_pos(self, pos=None):
        if pos is None:
            pos = (self.source.x + self.source_offset[0], self.source.y + self.source_offset[0])
        x_offset = pos[0] - self.x
        y_offset = pos[1] - self.y
        self.x = pos[0]
        self.y = pos[1]
        for item in self.items:
            new_pos = (item.x + x_offset, item.y + y_offset)
            item.update_pos(new_pos)

        self.close_button.x = self.x + self.width - self.padding - 10
        self.close_button.y = self.y + self.padding - 17


def mouse_handler(event_type: str, mouse_pos: tuple, mouse_buttons: tuple):
    global left_mouse_held
    global right_mouse_held
    global buttons
    global text_boxes
    global menu
    global tree
    global open_menu
    global draw_edge

    distance_to_node = 0
    for node in tree.nodes:
        if node.draw_edge:
            distance_to_node = ((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2)**0.5

    if event_type == 'down':
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
            # Left click background
            if not node_click:
                # Select menu item
                if menu is not None:
                    for item in menu.items:
                        item.blink_counter = 0
                        item.selected = False
                        if item.check_collide(mouse_pos):
                            item.selected = True
                    if menu.close_button.check_collide(mouse_pos):
                        menu = None

            # Pop buttons
            if len(buttons) != 0:
                if not buttons[0].check_collide(mouse_pos):
                    buttons.pop(0)

            # Left click Textbox
            for box in text_boxes:
                box.selected = False
                box.blink_counter = 0
                if box.check_collide(mouse_pos):
                    box.selected = True
        # Right click
        if mouse_buttons[2]:
            right_mouse_held = True
            node_click = False
            # Right click node
            for node in tree.nodes:
                if ((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2)**0.5 <= node.radius + 1:
                    node_click = True
                    open_menu = True
                    node.draw_edge = True
                    break
            # Right click background
            if not node_click:
                if len(buttons) == 0:
                    if not draw_edge:
                        buttons.append(Button(mouse_pos[0] + 7, mouse_pos[1], 'Node', action='node'))
                elif buttons[0].check_collide(mouse_pos):
                    buttons.pop(0)
                else:
                    buttons[0].x = mouse_pos[0] + 7
                    buttons[0].y = mouse_pos[1]
    elif event_type == 'up':
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
                        edge = tree.edges[len(tree.edges) - 1]
                        edge.source.draw_edge = False
                        edge.held = False
                        edge.target = node
                        edge.update_pos()
                        # Update nodes data
                        edge.source.children.append(edge.target)
                        edge.target.parents.append(edge.source)

                    # Open Node data menu
                    elif open_menu:
                        menu = Menu(mouse_pos[0], mouse_pos[1], 'node', node)
                        open_menu = False
                        node.draw_edge = False
                    elif node.draw_edge:
                        node.draw_edge = False
                    break

    # Button Actions
    pop_list = []
    for i in range(len(buttons)):
        buttons[i].mouse_input(mouse_pos, mouse_buttons, event_type)
        if buttons[i].run:
            if buttons[i].action == 'node':
                tree.nodes.append(Node(mouse_pos[0], mouse_pos[1], '', 0, held=True))
                pop_list.insert(0, i)
    for index in pop_list:
        buttons.pop(index)
    for button in buttons:
        button.draw()

    # Nodes / Edges
    for node in tree.nodes:
        if node.held:
            node.update_pos(mouse_pos)
        elif not draw_edge and node.draw_edge:
            if abs(distance_to_node) >= node.radius + 5:
                tree.edges.append(Edge(node.x, node.y, 0, 0, 3, node))
                draw_edge = True
                open_menu = False
        elif node.draw_edge:
            if abs(distance_to_node) <= node.radius + 1:
                draw_edge = False
                tree.edges.pop()
    if draw_edge:
        tree.edges[len(tree.edges) - 1].update_pos(mouse_pos)

    if menu is not None:
        menu.draw()
        menu.update_pos()


def debug_(variables: list):
    global debug

    changed = False
    if debug != variables:
        debug = variables
        print(debug)


tree = Tree()

if len(integers) < 0:
    menu = Menu(0, 0, '', Node(0, 0, '', 0))
else:
    menu = None
buttons = []
text_boxes = []
left_mouse_held = False
right_mouse_held = False
open_menu = False
draw_edge = False
held_key = ''
held_key_event = None
key_hold_counter = 0
running = True
while running:
    screen.fill(black)
    tree.draw_tree()

    for textbox in text_boxes:
        textbox.draw()

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

            # Update textboxes
            for textbox in text_boxes:
                if textbox.selected:
                    if keys[K_BACKSPACE]:
                        held_key = 'backspace'
                        key_hold_counter = frame_rate
                        textbox.update_text(backspace=True)
                    else:
                        held_key = event.unicode
                        held_key_event = event
                        key_hold_counter = frame_rate
                        textbox.update_text(event.unicode)
            if menu is not None:
                # Send input to Menu textbox
                for textbox in menu.items:
                    if textbox.selected:
                        if keys[K_BACKSPACE]:
                            held_key = 'backspace'
                            key_hold_counter = frame_rate
                            textbox.update_text(backspace=True)
                        elif textbox.label == 'Children':
                            if event.unicode in integers:
                                held_key = event.unicode
                                held_key_event = event
                                key_hold_counter = frame_rate
                                textbox.update_text(event.unicode)
                        else:
                            held_key = event.unicode
                            held_key_event = event
                            key_hold_counter = frame_rate
                            textbox.update_text(event.unicode)

                        # update node data
                        if textbox.label == 'Label':
                            menu.source.label = textbox.text
                        elif textbox.label == 'Children':
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

    mouse_handler('', pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    if held_key != '' and key_hold_counter == 0:
        key_hold_counter = frame_rate / 30
        for textbox in text_boxes:
            if textbox.selected:
                if held_key == 'backspace':
                    textbox.update_text(backspace=True)
                else:
                    textbox.update_text(held_key)
                break
        if menu is not None:
            for textbox in menu.items:
                if textbox.selected:
                    if held_key == 'backspace':
                        textbox.update_text(backspace=True)
                    else:
                        textbox.update_text(held_key)
                    break
    elif key_hold_counter > 0:
        key_hold_counter -= 1

    clock.tick(frame_rate)
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
