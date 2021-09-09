from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import glm
import pygame

# tamanho da tela
WINDOW_WIDHT = 1000
WINDOW_HEIGHT = 1000

# glm.vec3 - inicialização de um vetor de 3 dimensões


# camera
cameraPos = glm.vec3(0, 3.5, 30)
cameraFront = glm.vec3(0, 0, -1)
cameraUp = glm.vec3(0, 1, 0)
angle = 0

# mouse
old_mouse_x = 0
old_mouse_y = 0
angle_x = -1.57
angle_y = 1.57
mouse_speed = 0.1
mouse_sensitivity = 0.001

lamp_color = glm.vec3(10, 10, 10)


#textures
textures = {
    'piso': None,
    'geladeira': None,
    'fogao' : None,
    'maquinadelavar' : None,
    'teto': None,
    'parede': None,
    'quadro1': None,
    'porta1':None,
    'janela': None
}

fan_rotation = 0
door_angle = 0
window_angle = 0

half_width = WINDOW_WIDHT / 2
half_height = WINDOW_HEIGHT / 2


# U
def draw_wall(x0, y0, z0, x1, y1, z1):
    # GLBegin - Specifies the primitive or primitives that will be created 
    # from vertices presented between glBegin and the subsequent glEnd.

    # GL_QUADS - argument that specifies in which way the vertices are interpreted.
    # Treats each group of four vertices as an independent quadrilateral.

    # glVertex3f - Specify x, y, z, coordinates of a vertex.


    glBegin(GL_QUADS)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y0, z1)
    glVertex3f(x1, y1, z1)
    glVertex3f(x0, y1, z0)
    glEnd()

def draw_textured_wall(x0, y0, z0, x1, y1, z1, texture):
    # glEnable - enable or disable server-side GL capabilities

    # GL_TEXTURE_2D - If enabled and no fragment shader is active, two-dimensional 
    # texturing is performed (unless three-dimensional or cube-mapped texturing is 
    # also enabled).

    # gl_BindTexture - bind a named texture to a texturing target
    # Specifies the target to which the texture is bound.

    # glTexCoord — set the current texture coordinates


    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x0, y0, z0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x1, y0, z1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x1, y1, z1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x0, y1, z0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def draw_floor(x, y, z, width, length):
    glBegin(GL_QUADS)
    glVertex3f(x, y, z)
    glVertex3f(x, y, z + length)
    glVertex3f(x + width, y, z + length)
    glVertex3f(x + width, y, z)
    glEnd()

def draw_textured_floor(x, y, z, width, length, texture):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, y, z + length)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x + width, y, z + length)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x + width, y, z)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def draw_block(x, y, z, width, length, height):
    draw_wall(x, y, z, x, y + height, z+length)
    draw_wall(x, y, z, x+width, y + height, z)
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    draw_floor(x, y, z, width, length)
    draw_floor(x, y+height, z, width, length)

def draw_texturized_block_right(x, y, z, width, length, height, texture):
    # glColor3f - set the current color (GLfloat red, GLfloat green, GLfloat blue)

    
    #left side
    draw_wall(x, y, z, x, y + height, z+length)
    #back side
    draw_wall(x, y, z, x+width, y + height, z)
    #front side
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    #down side
    draw_floor(x, y, z, width, length)
    #up side
    draw_floor(x, y+height, z, width, length)
    #right side
    glColor3f(1, 1, 1)
    draw_textured_wall(x+width, y, z, x + width, y + height, z + length, texture)

def draw_texturized_block_front(x, y, z, width, length, height, texture):
    #left side
    draw_wall(x, y, z, x, y + height, z+length)
    #back side
    draw_wall(x, y, z, x+width, y + height, z)
    #right side
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    #down side
    draw_floor(x, y, z, width, length)
    #up side
    draw_floor(x, y+height, z, width, length)
    # front side
    glColor3f(1, 1, 1)
    draw_textured_wall(x, y, z+length, x + width, y + height, z + length, texture)

def draw_texturized_block_front_and_back(x, y, z, width, length, height, texture_front, texture_back):
    #left side
    draw_wall(x, y, z, x, y + height, z+length)
    #right side
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    #down side
    draw_floor(x, y, z, width, length)
    #up side
    draw_floor(x, y+height, z, width, length)
    # front side
    glColor3f(1, 1, 1)
    draw_textured_wall(x, y, z+length, x + width, y + height, z + length, texture_front)
    #back side
    draw_textured_wall(x, y, z, x+width, y + height, z, texture_back)

def draw_texturized_block_up(x, y, z, width, length, height, texture):
    #left side
    draw_wall(x, y, z, x, y + height, z+length)
    #back side
    draw_wall(x, y, z, x+width, y + height, z)
    #right side
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    #down side
    draw_floor(x, y, z, width, length)
    # front side
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    #up side
    glColor3f(1, 1, 1)
    draw_textured_floor(x, y+height, z, width, length, texture)

def draw_colored_block(x, y, z, width, length, height, front_color, back_color, left_color, right_color, up_color, down_color):
    #left side
    glColor3f(left_color.x, left_color.y, left_color.z)
    draw_wall(x, y, z, x, y + height, z+length)
    #back side
    glColor3f(back_color.x, back_color.y, back_color.z)
    draw_wall(x, y, z, x+width, y + height, z)
    #right side
    glColor3f(right_color.x, right_color.y, right_color.z)
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    #front side
    glColor3f(front_color.x, front_color.y, front_color.z)
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    #down side
    glColor3f(down_color.x, down_color.y, down_color.z)
    draw_floor(x, y, z, width, length)
    #up side
    glColor3f(up_color.x, up_color.y, up_color.z)
    draw_floor(x, y+height, z, width, length)

def draw_colored_block_fixed(x, y, z, width, length, height):
    glColor3f(0.293, 0.211, 0.13)
    draw_wall(x, y, z, x, y + height, z+length)
    glColor3f(0.486, 0.293, 0)
    draw_wall(x, y, z, x+width, y + height, z)
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    glColor3f(0.36, 0.2, 0.09)
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    draw_floor(x, y, z, width, length)
    glColor3f(0.37, 0.15, 0.07)
    draw_floor(x, y+height, z, width, length)

def draw_cylinder(x, y, z, radius, height):
    px = 0
    pz = 0
    c_angle = 0
    angle_stepsize = 0.1


    # GLBegin - Specifies the primitive or primitives that will be created 
    # from vertices presented between glBegin and the subsequent glEnd.

    # GL_QUADS_STRIP - Draws a connected group of quadrilaterals. One quadrilateral 
    # is defined for each pair of vertices presented after the first pair. Vertices 2 
    # ⁢ n - 1 , 2 ⁢ n , 2 ⁢ n + 2 , and 2 ⁢ n + 1 define quadrilateral n. N 2 - 1 
    # quadrilaterals are drawn. Note that the order in which vertices are used to 
    # construct a quadrilateral from strip data is different from that used with 
    # independent data


    #desenha cilindro
    glBegin(GL_QUAD_STRIP)
    c_angle = 0
    while c_angle < 2*glm.pi() + 1:
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y + height, z + pz)
        glVertex3f(x + px, y, z + pz)
        c_angle += angle_stepsize
    glEnd()


    # GL_POLYGON - Draws a single, convex polygon. Vertices 1 through N define this 
    # polygon.


    #desenha tampa do cilindro
    glBegin(GL_POLYGON)
    c_angle = 0
    while c_angle < 2*glm.pi():
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y + height, z + pz)
        c_angle += angle_stepsize
    glEnd()


    # GL_POLYGON - Draws a single, convex polygon. Vertices 1 through N define this 
    # polygon.


    #desenha fundo do cilindro
    glBegin(GL_POLYGON)
    c_angle = 0
    while c_angle < 2 * glm.pi():
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y, z + pz)
        c_angle += angle_stepsize
    glEnd()

def draw_fan(x, y, z, rot):
    # glPushMatrix - push the current matrix stack

    # glPopMatrix() - pop the current matrix stack

    # glTranslate - multiply the current matrix by a translation matrix

    # glColor - set the current color glColor3ub(GLubyte red, GLubyte green, GLubyte blue);

    # glRotatef - glRotate — multiply the current matrix by a rotation matrix
    # glRotatef( GLfloat angle, GLfloat x, GLfloat y, GLfloat z);

    # glScale - multiply the current matrix by a general scaling matrix
    # glScalef(	GLfloat x, GLfloat y, GLfloat z);

    # glutPostRedisplay - Mark the normal plane of current window as needing to be 
    # redisplayed. The next iteration through glutMainLoop, the window's display 
    # callback will be called to redisplay the window's normal plane.


    #begin fan
    glPushMatrix() 
    glTranslatef(x, y, z)

    # motor + helices
    glPushMatrix() 
    glColor3ub(80, 80, 80)
    glTranslatef(0, 6, -12)
    glRotatef(180, 1, 0, 0)
    draw_cylinder(0, 1.7, 0, 0.4, 0.8) #motor
    glColor3ub(10, 10, 10)
    draw_cylinder(0, 2.5, 0, 0.05, 0.1)  # haste helices

    glRotatef(-rot, 0, 1, 0) #<<<<ISSO AQUI RODA O VENLILADOR
    glPushMatrix() #push helices
    glColor3ub(100, 100, 100)
    draw_cylinder(0, 2.6, 0, 0.3, 0.2)  # centro helices
    glColor3ub(130, 130, 130)
    glPushMatrix()
    glScalef(2, 1, 1)
    draw_cylinder(-0.45, 2.7, 0, 0.3, 0.03)# helice 1
    draw_cylinder(0.45, 2.7, 0, 0.3, 0.03)  # helice 2
    glPopMatrix()
    glScalef(1, 1, 2)
    draw_cylinder(0, 2.7, 0.45, 0.3, 0.03)  # helice 3
    draw_cylinder(0, 2.7, -0.45, 0.3, 0.03)   # helice 4
    glPopMatrix() #pop helices
    glutPostRedisplay()
    glPopMatrix() #pop motor

    glPopMatrix() #end fan
    
def draw_chair(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    #assento
    draw_colored_block_fixed(0, 1, 0, 1.2, 1, 0.1)
    #pés
    draw_colored_block_fixed(0, 0, 0, 0.2, 0.2, 1)
    draw_colored_block_fixed(1, 0, 0, 0.2, 0.2, 1)
    draw_colored_block_fixed(0, 0, 0.8, 0.2, 0.2, 1)
    draw_colored_block_fixed(1, 0, 0.8, 0.2, 0.2, 1)
    #encosto
    draw_colored_block_fixed(0, 1.1, 0.9, 1.2, 0.1, 1.5)
    glPopMatrix()

def draw_lamp(x, y, z, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(100, 100, 100)
    draw_cylinder(0, 0, 0, 0.3, 0.1) # base

    glColor3ub(60, 60, 60)
    draw_cylinder(0, 0.1, 0, 0.05, 0.6) #haste

    glPushMatrix()
    glColor3ub(80, 80, 80)
    glTranslatef(0, 0.8, -1.85)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0, 1.7, 0, 0.15, 0.4) # corpo da lampada
    glColor3f(color.x/255, color.y/255, color.z/255)
    draw_cylinder(0, 2.1, 0, 0.1, 0.01)  # frente da lampada
    glPopMatrix()

    glPopMatrix()


# F
def draw_table1(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(250, 250, 250)
    #tampo
    draw_block(0, 2, 0, 3, 3, 0.1)
    #pé esquerdo trás
    draw_block(0, 0, 0, 0.3, 0.1, 2)
    draw_block(0, 0, 0, 0.1, 0.3, 2)
    #pé esquerdo frente
    glPushMatrix()
    glTranslatef(0, 0, 3)
    glRotatef(90, 0, 1, 0)
    draw_block(0, 0, 0, 0.3, 0.1, 2)
    draw_block(0, 0, 0, 0.1, 0.3, 2)
    glPopMatrix()
    #pé direito trás
    glPushMatrix()
    glTranslatef(3, 0, 0)
    glRotatef(270, 0, 1, 0)
    draw_block(0, 0, 0, 0.3, 0.1, 2)
    draw_block(0, 0, 0, 0.1, 0.3, 2)
    glPopMatrix()
    #pé direito frente
    glPushMatrix()
    glTranslatef(3, 0, 3)
    glRotatef(180, 0, 1, 0)
    draw_block(0, 0, 0, 0.3, 0.1, 2)
    draw_block(0, 0, 0, 0.1, 0.3, 2)
    glPopMatrix()

    glPopMatrix() # fim fan_table

def draw_refrigerator(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(250, 250, 250)
    draw_texturized_block_right(0, 0, 0, 2, 2.5, 5, textures['geladeira'])
    glPopMatrix()

def draw_stove(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(250, 250, 250)
    draw_texturized_block_right(0, 0, 0, 2, 2, 2.5, textures['fogao'])
    glPopMatrix()

def draw_maquinaDeLavar(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(250, 250, 250)
    draw_texturized_block_right(0, 0, 0, 2, 2, 2.5, textures['maquinadelavar'])
    glPopMatrix()

def draw_sink(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3ub(250, 250, 250)
    # pia lado esquerdo
    draw_colored_block_fixed(0, 2, 0, 1.25, 2, 0.1)
    # pia baixo
    draw_colored_block_fixed(1.25, 1.50, 0, 1, 1.50, 0.1)
    # pia lado direito
    draw_colored_block_fixed(2.25, 2, 0, 1.25, 2, 0.1)
    # pia baixo lado esquerdo
    draw_colored_block_fixed(1.15, 1.50, 0, 0.1, 1.50, 0.60)
    # pia baixo lado direito
    draw_colored_block_fixed(2.25, 1.50, 0, 0.1, 1.50, 0.60)
    # pia fundo
    draw_colored_block_fixed(1.25, 1.50, 0, 1, 0.10, 0.60)
    # pia frente
    draw_colored_block_fixed(1.25, 1.50, 1.40, 1, 0.10, 0.60)
    # pia frente horizontal
    draw_colored_block_fixed(1.25, 2, 1.40, 1, 0.60, 0.1)
    glPopMatrix()


def display():
    # glClear - clear buffers to preset values Bitwise OR of masks that
    # indicate the buffers to be cleared.
    # GL_COLOR_BUFFER_BIT - Indicates the buffers currently enabled for color writing.
    # GL_DEPTH_BUFFER_BIT - Indicates the depth buffer.

    # glLoadIdentity - replace the current matrix with the identity matrix

    # gluLookAt - define a viewing transformation
    # eyeX, eyeY, eyeZ - Specifies the position of the eye point.
    # centerX, centerY, centerZ - Specifies the position of the reference point.
    # upX, upY, upZ - Specifies the direction of the up vector.
    
    #  glutSwapBuffers - swaps the buffers of the current window if double buffered.


    global angle, texture_brick, fan_rotation, door_angle, window_angle
    # limpa cor e buffers de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # reseta transformações
    glLoadIdentity()

    # define camera
    # camx camy camz centerx centery centerz upx upy upz
    gluLookAt(cameraPos.x, cameraPos.y, cameraPos.z,
              cameraPos.x + cameraFront.x, cameraPos.y + cameraFront.y, cameraPos.z + cameraFront.z,
              cameraUp.x, cameraUp.y, cameraUp.z)


    glPushMatrix() # push cozinha
    # piso
    glColor(1, 1, 1)
    draw_textured_floor(-10, 0, -10, 20, 20, textures['piso'])

    # parede de trás
    glColor3ub(255, 255, 255)
    draw_textured_wall(-10, 0, -10, 10, 7, -10, textures['parede'])

    # parede esquerda
    glColor3ub(250, 250, 250)
    draw_textured_wall(-10, 0, -10, -10, 7, 10, textures['parede'])

    # parede da frente com portas e janelas
    glColor3ub(221,217,206)
    # part1 -  parte esquerda parede porta
    draw_block(-10, 0, 10, 2, 0.4, 7)
    # part2 - parte superior parede porta 
    draw_block(-8, 5, 10, 3, 0.4, 2)
    # part3 - parte direita parede porta
    draw_block(-5, 0, 10, 2, 0.4, 7)
    # part4 - parte cima da janela
    draw_block(-3, 5, 10, 4, 0.4, 2)
    # part5 - parte baixo janela
    draw_block(-3, 0, 10, 4, 0.4, 2.5)
    # part6 - restante da parede
    draw_block(1, 0, 10, 9, 0.4, 7)

   
    # alisais esquerdo - suporte porta lado esquerdo
    draw_colored_block_fixed(-8, 0, 10, 0.1, 0.4, 5)
    # alisais direito - suporte porta direito
    draw_colored_block_fixed(-5.1, 0, 10, 0.1, 0.4, 5)
    # alisais topo - suporte porta lado topo
    draw_colored_block_fixed(-7.9, 4.9, 10, 2.8, 0.4, 0.1)


    # alisais esquerdo - suporte janela lado esquerdo
    draw_colored_block_fixed(-3, 2.5, 10, 0.1, 0.4, 2.5)
    # alisais direito - suporte janela lado direito
    draw_colored_block_fixed(0.9, 2.5, 10, 0.1, 0.4, 2.5)
    # alisais baxio - suporte janela baixo
    draw_colored_block_fixed(-3, 2.5, 10, 4, 0.4, 0.1)
    # alisais cima - suporte janela cima
    draw_colored_block_fixed(-3, 4.9, 10, 4, 0.4, 0.1)

    #porta principal
    glPushMatrix()
    glTranslatef(-7.9, 0, 10)
    glRotatef(door_angle, 0, 1, 0)
    draw_texturized_block_front_and_back(0,0,0, 2.8, 0.1, 4.9, textures['porta1'], textures['porta1'])
    glPopMatrix()

    #janela 
    glPushMatrix()
    glTranslatef(-2.9, 4.9, 10)
    glRotatef(-window_angle, 1, 0, 0)
    glColor3ub(70, 35, 26)
    draw_texturized_block_front_and_back(0, 0, 0, 3.8, 0.1, -2.3, textures['janela'], textures['janela'])
    glPopMatrix()

    # parede direita
    glColor3ub(245, 245, 245)
    draw_textured_wall(10, 0, -10, 10, 7, 10, textures['parede'])

    # teto
    glColor3ub(250, 250, 250)
    draw_textured_floor(-10, 7, -10, 20, 20, textures['teto'])

    # mesa no centro
    glPushMatrix()
    glTranslatef(1.3, 0, 0)
    glRotatef(180, 0, 1, 0)
    draw_table1(0, 0, 0)
    # cadeira
    glRotatef(90, 0, 1, 0)
    draw_chair(-2, 0, 2.5)
    glPopMatrix()

    # Geladeira
    glPushMatrix()
    glTranslatef(-3, 0, -9.8)
    glRotatef(-90, 0, 1, 0)
    draw_refrigerator(0, 0, 0)
    glPopMatrix()

    # Fogão
    glPushMatrix()
    glTranslatef(4, 0, -9.8)
    glRotatef(-90, 0, 1, 0)
    draw_stove(0, 0, 0)
    glPopMatrix()

    # Maquina de lavar
    glPushMatrix()
    glTranslatef(7, 0, -9.8)
    glRotatef(-90, 0, 1, 0)
    draw_maquinaDeLavar(0, 0, 0)
    glPopMatrix()

    # Pia
    glPushMatrix()
    glTranslatef(-2, 0, -10)
    draw_sink(0, 0, 0)
    glPopMatrix()
    
    # Quadro
    glPushMatrix()
    glColor3ub(255, 255, 255)
    draw_texturized_block_front(-1, 4, -9.99, 2, 0.05, 2, textures['quadro1'])
    glPopMatrix()

    # Ventilador
    glPushMatrix()
    glTranslatef(-1.3, 0, 9.9)
    draw_fan(2, 2.3, 1.3, fan_rotation)
    glPopMatrix()

    # Lampada
    glPushMatrix()

    draw_lamp(0, 2.1, -2, lamp_color)
    glPopMatrix()

    # incrementa a variavel de rotação do ventilador
    if fan_rotation >= 360:
        fan_rotation = 0.0
    fan_rotation += 1 #velocidade da rotação

    glPopMatrix()  # pop quarto

    glutSwapBuffers()

def keyboard(key, x, y):
    # glm.cross - Returns the cross product of x and y.

    # glm.normalize - Returns a vector in the same direction as x but with length of 1.

    # glEnable - enable or disable server-side GL capabilities
    # GL_LIGHTi - If enabled, include light i in the evaluation of the 
    # lighting equation.

    # glutPostRedisplay - Mark the normal plane of current window as needing to be 
    # redisplayed. The next iteration through glutMainLoop, the window's display 
    # callback will be called to redisplay the window's normal plane.


    global angle, cameraFront, cameraUp, cameraPos, door_angle, window_angle, light_ambient, light_specular, light_diffuse, lamp_color

    cameraSpeed = 0.5

    if not isinstance(key, int):
        key = key.decode("utf-8")
    #controles da camera
    if key == 'w' or key == 'W':
        cameraPos += cameraSpeed * cameraFront
    elif key == 'a' or key == 'A':
        cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    elif key == 's' or key == 'S':
        cameraPos -= cameraSpeed * cameraFront
    elif key == 'd' or key == 'D':
        cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    elif key == 'q' or key == 'Q':
        cameraPos.y += cameraSpeed/2
    elif key == 'e' or key == 'E':
        cameraPos.y -= cameraSpeed/2

    #abertura da porta
    if key == 'o':
        door_angle += 5
    if key == 'O':
        door_angle -= 5
    #abertura das janelas
    if key == 'j':
        window_angle += 5
    if key == 'J':
        window_angle -= 5
    #controle da iluminação
    if key == 'i':
        glEnable(GL_LIGHT0)
    if key == 'I':
        glDisable(GL_LIGHT0)
    #controle spotlight
    if key == 'l':
        lamp_color = glm.vec3(255, 255, 255)
        glEnable(GL_LIGHT1)
    if key == 'L':
        lamp_color = glm.vec3(10, 10, 10)
        glDisable(GL_LIGHT1)


    glutPostRedisplay()


def change_side(w, h):
    # glMatrixMode - specify which matrix is the current matrix
    # GL_MODELVIEW - Applies subsequent matrix operations to the 
    # modelview matrix stack.
    
    # glLoadIdentity - replace the current matrix with the identity matrix

    # glViewport - set the viewport 
    # glViewport(GLint x, GLint y, GLsizei width, GLsizei height);

    # gluPerspective - set up a perspective projection matrix
    # gluPerspective(GLdouble fovy, GLdouble aspect, GLdouble zNear, GLdouble zFar);

    global half_width, half_height
    if h == 0:
        h = 1
    ratio = w * 1/h

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    glViewport(0, 0, w, h)

    half_width = w / 2
    half_height = h / 2

    gluPerspective(45, ratio, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)


def mouse_click(button, state, x, y):
    global old_mouse_x, old_mouse_y
    old_mouse_x = x
    old_mouse_y = y


def mouse_camera(mouse_x, mouse_y):
    global mouse_sensitivity, mouse_speed, angle_x, angle_y, cameraFront, old_mouse_x, old_mouse_y

    angle_x -= (mouse_x - old_mouse_x) * mouse_sensitivity
    angle_y -= (mouse_y - old_mouse_y) * mouse_sensitivity

    if angle_y > 2:
        angle_y = 2
    if angle_y < 1:
        angle_y = 1

    front = glm.vec3()
    front.x = glm.cos(angle_x) * glm.sin(angle_y)
    front.z = glm.sin(angle_x) * glm.sin(angle_y)
    front.y = glm.cos(angle_y)
    cameraFront = front

    old_mouse_x = mouse_x
    old_mouse_y = mouse_y
    glutPostRedisplay()


def load_texture(image):
    # pygame.image.load - load new image from a file

    # pygame.image.tostring - transfer image to string buffer

    # glGenTextures - generate texture names 
    # glGenTextures( GLsizei n, GLuint * textures);
    # n - Specifies the number of texture names to be generated.

    # gl_BindTexture - bind a named texture to a texturing target
    # Specifies the target to which the texture is bound.

    # glPixelStorei - set pixel storage modes
    # glPixelStorei(GLenum pname, GLint param);
    # pname - Specifies the symbolic name of the parameter to be set. 
    # One value affects the packing of pixel data into memory: GL_PACK_ALIGNMENT. 
    # The other affects the unpacking of pixel data from memory: GL_UNPACK_ALIGNMENT.
    # param - Specifies the value that pname is set to.

    # GL_UNPACK_ALIGNMENT - Specifies the alignment requirements for the 
    # start of each pixel row in memory. The allowable values are 1 (byte-alignment), 
    # 2 (rows aligned to even-numbered bytes), 4 (word-alignment), 
    # and 8 (rows start on double-word boundaries).

    # glTexParameter - set texture parameters
    # glTexParameterf(GLenum target, GLenum pname, GLfloat param)
    # target - Specifies the target texture
    # pname - Specifies the symbolic name of a single-valued texture parameter.
    # param - Specifies the value of pname.

    # GL_TEXTURE_2D - If enabled and no fragment shader is active, two-dimensional 
    # texturing is performed (unless three-dimensional or cube-mapped texturing is 
    # also enabled).

    # GL_TEXTURE_WRAP_S - Sets the wrap parameter for texture coordinate s 
    # GL_MIRRORED_REPEAT -  causes the s coordinate to be set to the fractional 
    # part of the texture coordinate if the integer part of s is even; if the integer 
    # part of s is odd, then the s texture coordinate is set to 1−frac(s),
    # where frac(s) represents the fractional part of s.

    # GL_TEXTURE_WRAP_T - Sets the wrap parameter for texture coordinate t 

    # GL_TEXTURE_MAG_FILTER - The texture magnification function is used whenever 
    # the level-of-detail function used when sampling from the texture determines 
    # that the texture should be magified. It sets the texture magnification function 
    # to either GL_NEAREST or GL_LINEAR (see below). GL_NEAREST is generally faster 
    # than GL_LINEAR, but it can produce textured images with sharper edges because 
    # the transition between texture elements is not as smooth. The initial value of 
    # GL_TEXTURE_MAG_FILTER is GL_LINEAR.

    # GL_LINEAR -Returns the weighted average of the texture elements that are closest
    #  to the specified texture coordinates. These can include items wrapped or 
    # repeated from other parts of a texture, depending on the values of GL_TEXTURE_WRAP_S 
    # and GL_TEXTURE_WRAP_T, and on the exact mapping.

    # GL_TEXTURE_MIN_FILTER - The texture minifying function is used whenever the level-of-detail 
    # function used when sampling from the texture determines that the texture should be minified. 
    # There are six defined minifying functions. Two of them use either the nearest texture elements or
    # a weighted average of multiple texture elements to compute the texture value. The other four use mipmaps.

    # GL_LINEAR_MIPMAP_LINEAR - Chooses the mipmap that most closely matches the size of the pixel being 
    # textured and uses the GL_LINEAR criterion (a weighted average of the four texture elements that are 
    # closest to the specified texture coordinates) to produce a texture value.

    # glTextEnvf - set texture environment parameters
    # glTexEnvf(GLenum target, GLenum pname, GLfloat param);
    # target - Specifies a texture environment.
    # name - Specifies the symbolic name of a texture environment parameter
    # params - Specifies a pointer to a parameter array that contains either a 
    # single symbolic constant, single floating-point number, or an RGBA color

    # glTexImage2D - specify a two-dimensional texture image
    # glTexImage2D(	GLenum target, GLint level,	GLint internalformat,
    # GLsizei width, GLsizei height, GLint border, GLenum format,
    # GLenum type, const void * data);

    # target - Specifies the target texture.
    # level - Specifies the level-of-detail number. Level 0 is the base image level. 
    # Level n is the nth mipmap reduction image

    # internalformat - Specifies the number of color components in the texture. 

    # width - Specifies the width of the texture image. All implementations support 
    # texture images that are at least 1024 texels wide.

    # height - Specifies the height of the texture image, or the number of layers 
    # in a texture array

    # border - This value must be 0.

    # format - Specifies the format of the pixel data

    # type - Specifies the data type of the pixel data

    # data - Specifies a pointer to the image data in memory.

    # glGenerateMipmap - generate mipmaps for a specified texture object
    # target - Specifies the target to which the texture object is bound for 
    # glGenerateMipmap

    textureSurface = pygame.image.load(image)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glGenerateMipmap(GL_TEXTURE_2D)

    return texid


def setup_lighting():
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 1])

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.8, 0.8, 0.8, 1])

    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.3, 0.3, 0.3, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 7, 0, 1])


    #spot light
    # spot light
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1, 1, 1, 1])

    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, [0, -1, 0])
    glLightfv(GL_LIGHT1, GL_POSITION, [0, 6, -1])

    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 20)
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 2.0)


def main():
    global textures

    # inicialização
    glutInit()  # inicia glut
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(WINDOW_WIDHT, WINDOW_HEIGHT)
    window = glutCreateWindow("Cozinha")

    #iluminação
    setup_lighting()

    #callbacks
    glutDisplayFunc(display)
    glutReshapeFunc(change_side)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse_click)
    glutMotionFunc(mouse_camera)

    #textures
    textures['piso'] = load_texture("textures/Tiles081.jpg")
    textures['geladeira'] = load_texture("textures/geladeira3.png")
    textures['fogao'] = load_texture("textures/fogao3.png")
    textures['maquinadelavar'] = load_texture("textures/maquinaDeLavar.jpg")
    textures['teto'] = load_texture("textures/Wood0054.jpg")
    textures['parede'] = load_texture("textures/Tiles093.jpg")
    textures['quadro1'] = load_texture("textures/quadro1.jpg")
    textures['porta1'] = load_texture("textures/door4.jpg")
    textures['janela'] = load_texture("textures/janela4.jpg")

    glutMainLoop()


main()
