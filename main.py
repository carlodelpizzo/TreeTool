import pygame
from pygame.locals import *


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
blue = [0, 0, 255]
grid_color = [50, 50, 50]
# Font
default_font = 'Helvetica'


class Node:
    def __init__(self, x_pos: int, y_pos: int, label: str, level: int, parents=None, children=None):
        self.x = x_pos
        self.y = y_pos
        self.label = label
        self.level = level
        if parents is None:
            self.parents = []
        else:
            self.parents = parents
        if children is None:
            self.children = []
        else:
            self.children = children

    def update_pos(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]

    def draw(self):
        pygame.draw.circle(screen, blue, (self.x, self.y), 10)


class Tree:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def draw_tree(self):
        for node in self.nodes:
            node.draw()


class Button:
    def __init__(self, x: int, y: int, label: str, padding=5, border_width=3, border_color=None,
                 button_color=None, font=default_font, font_size=20, font_color=None, action=None):
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
        self.run = False
        self.pressed = False
        self.pressed_draw = False

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

    def update_pos(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]


class TextBox:
    def __init__(self, x_pos, y_pos, label='', text='', padding=5, border_width=3):
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

        self.selected = True
        self.cursor_pos = self.text_width + self.x + self.padding + 2
        self.blink_counter = 0
        self.text_input_counter = 0

    def draw(self):
        # Draw Label
        screen.blit(self.font.render(self.label + ':', True, self.color),
                    (self.x, self.y + self.padding))
        # Draw background
        pygame.draw.rect(screen, self.bg_color, (self.x + self.label_offset, self.y, self.width, self.height))

        # Draw border
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

        # Draw text
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
        self.text_input_counter = int(frame_rate * 1.5)
        self.text += character
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


class Menu:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.items = []


def mouse_handler(event_type: str, mouse_pos: tuple, mouse_buttons: tuple):
    global left_mouse_held
    global right_mouse_held
    global held_objects
    global buttons
    global text_boxes

    if event_type == 'down':
        if len(held_objects) > 0:
            for i in range(len(held_objects)):
                tree.nodes.append(held_objects[i])
            held_objects = []
        # Left click
        if mouse_buttons[0]:
            left_mouse_held = True

            # Textboxes
            for box in text_boxes:
                box.selected = False
                box.blink_counter = 0
                if box.check_collide(mouse_pos):
                    box.selected = True
        # Right click
        if mouse_buttons[2]:
            right_mouse_held = True
            node_click = False
            for node in tree.nodes:
                if node.x - 7 <= mouse_pos[0] <= node.x + 7 and node.y - 7 <= mouse_pos[1] <= node.y + 7:
                    node_click = True
                    break
            if not node_click:
                if len(buttons) == 0:
                    buttons.append(Button(mouse_pos[0], mouse_pos[1], 'Node', action='node'))
                else:
                    if buttons[0].check_collide(mouse_pos):
                        buttons.pop(0)
                    else:
                        buttons[0].x = mouse_pos[0]
                        buttons[0].y = mouse_pos[1]
    elif event_type == 'up':
        if not mouse_buttons[0]:
            left_mouse_held = False
        if not mouse_buttons[2]:
            right_mouse_held = False

    # Buttons
    pop_list = []
    for i in range(len(buttons)):
        buttons[i].mouse_input(mouse_pos, mouse_buttons, event_type)
        if buttons[i].run:
            if buttons[i].action == 'node':
                held_objects.append(Node(mouse_pos[0], mouse_pos[1], 'temp', 0))
                pop_list.insert(0, i)
    for index in pop_list:
        buttons.pop(index)
    for button in buttons:
        button.draw()

    # Update held objects pos
    for item in held_objects:
        item.update_pos(mouse_pos)
        item.draw()


tree = Tree()
buttons = []
text_boxes = [TextBox(100, 100, label='Test', text='gabagool')]
held_objects = []
left_mouse_held = False
right_mouse_held = False
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
    elif key_hold_counter > 0:
        key_hold_counter -= 1

    clock.tick(frame_rate)
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
