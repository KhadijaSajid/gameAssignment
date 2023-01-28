import sys
from panda3d.core import *
loadPrcFile("conf.prc")
from direct.showbase.ShowBase import *
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import *
from direct.actor.Actor import Actor
from math import *

keyMap = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "rotate": False,
    "running":False,
    "walking": False,


}
def updateKeyMap(key, state):
    keyMap[key] = state


class MyGame(ShowBase):
    def __init__(self):
        super().__init__()
        
        self.setBackgroundColor(0.1,0.1,0.1,1)

        self.box = self.loader.loadModel("models/box")
        self.x  = 0
        self.speed = 5
        self.angle = 0
        self.myFrame= None
        self.startBtn = 0
        self.splashScreenimg = None
        self.text = None
        self.font = self.loader.loadFont("assets/Wbxkomik.ttf")
        self.disableMouse()  
        self.tx = 0.0
        self.tx_offset = 1/6
        self.texture_update = 0
        self.plane = 0
        self.tex = 0

        self.panda = self.loader.loadModel("models/panda")

        
        self.eve = Actor("Model/eve", 
                         {'walk': "Model/eve_walk", "run": "Model/eve_run"} )
                         

        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        self.render.setLight(self.ambientLightNodePath)
        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)
        render.setShaderAuto()

        self.taskMgr.doMethodLater(0.1, self.splash1, 'destroyLabel')
        # self.taskMgr.doMethodLater(0.1, self.mainScreen, 'destroyLabel')

        # self.loadAudio()

        # keyboard events 
        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])

        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])

        self.accept("arrow_up", updateKeyMap, ["up", True])
        self.accept("arrow_up-up", updateKeyMap, ["up", False])

        self.accept("arrow_down", updateKeyMap, ["down", True])
        self.accept("arrow_down-up", updateKeyMap, ["down", False])
        
        self.accept("space", updateKeyMap, ["rotate", True])
        self.accept("space-up", updateKeyMap, ["rotate", False])

        self.accept("r", updateKeyMap, ["running", True])
        self.accept("r-up", updateKeyMap, ["running", False])
        
        self.accept("w", updateKeyMap, ["walking", True])
        self.accept("w-up", updateKeyMap, ["walking", False])

        self.speed = 4
        self.angle = 0
        self.taskMgr.add(self.keyboardEvent, "keyboardEvent")

   
        
    def mainScreen(self, a):
        self.text.destroy()
        myText = OnscreenText(text='NCT 127 \n\n Raise The Roof', parent=self.myFrame,pos=(0,0.5),scale=.1, fg = (0.1,0.35,0.35,1),shadow= (0,0,0,1), font=self.font)
        exitBtn = DirectButton(geom=self.loadImageAsPlane('./assets/exit.png'), relief=None, command= self.exitBtnOnClick)
        exitBtn.setTransparency(TransparencyAttrib.MAlpha)        
        exitBtn.setPos(0.3,0,-0.5)
        self.startBtn = DirectButton(geom=self.loadImageAsPlane('./assets/start.png'), relief=None, command= self.startBtnOnClick,  extraArgs=[self.myFrame, exitBtn, myText])
        self.startBtn.setTransparency(TransparencyAttrib.MAlpha)
        self.startBtn.setPos(-0.3,0,-0.5)
        self.box.reparentTo(render)
        self.camera.setPos(0, -10, -0.5)
        self.box.setScale(0.6, 0.6,0.6)
        self.box.setColor(0.6,0.5,1,1)
        self.taskMgr.add(self.rotateSphere, "rotateSphere")

    

    def splash1(self,a):
        self.splashScreenimg=OnscreenImage(image = './assets/eyeMovie.gif', pos = (0, 0, 0.2), scale=0.5 ,parent=render2d)
        self.splashScreenimg.setTransparency(True)
        taskMgr.doMethodLater(1, self.splash2, 'mainScreen')

    def splash2(self, a):
        self.splashScreenimg.destroy()
        self.text = OnscreenText(text='Khadija Sajid \n\n B19102049 \n\n Computer graphics \n\n Miss humera tariq', parent=render2d,pos=(0,0.25), scale=0.1, fg = (0.91,0.35,0.21,1),
        shadow= (0,0,0,1), font=self.font)
        taskMgr.doMethodLater(1, self.mainScreen, 'mainScreen' )

    def rotateSphere(self, task):
        dt = globalClock.getDt()
        self.box.setH(self.angle)
        # self.box.setPos(cos(self.y)*2, sin(self.y)*2, -1)
        self.box.setPos(-1, cos(self.x)*2, sin(self.x)*2)

        self.angle += 1
        self.x += self.speed * dt
        return task.cont

    def startBtnOnClick(self, frame, deleteBtn, Text):
        render.getChildren().detach()

        # self.myFrame.destroy()
        self.startBtn.destroy()
        deleteBtn.destroy()
        Text.destroy()
        taskMgr.doMethodLater(0.1, self.gameScreen, 'gameScreen')
        # taskMgr.doMethodLater(0.1, self.spriteAnimation, 'gameScreen')



    def exitBtnOnClick(self):
        sys.exit()

    def gameScreen(self, task):
        self.camera.setPos(0, -15, 2)
        self.camera.reparentTo(render)
        self.eve.reparentTo(render)  # Put it in the scene
        self.onekeyText = self.genLabelText("[left arrow]: Move left", 1)
        self.onekeyText = self.genLabelText("[right arrow]: Move right", 2)
        self.twokeyText = self.genLabelText("[up arrow]: Move up", 3)
        self.threekeyText = self.genLabelText("[down arrow]: Move down", 4)
        self.threekeyText = self.genLabelText("[space bar]: Rotate", 5)
        self.fourkeyText = self.genLabelText("[W]: Walk", 6)
        self.fourkeyText = self.genLabelText("[R]: Run", 7)
       

        self.eve.actorInterval("walk", playRate=2).loop()



    def genLabelText(self, text, i):
        return OnscreenText(text=text, parent=base.a2dTopLeft, scale=.05,
                        pos=(0.06, -.08 * i), fg=(1, 1, 1, 1),
                        shadow=(0, 0, 0, 1), align=TextNode.ALeft, font=self.font)
    def keyboardEvent(self, task):
        dt = globalClock.getDt()
        pos = self.eve.getPos()
        if keyMap["left"]:
            pos.x -= self.speed *dt
            self.angle = -60
            self.eve.setH(self.angle)
        if keyMap["right"]:
            self.angle = 60
            self.eve.setH(self.angle)
            pos.x += self.speed *dt
        if keyMap["up"]:
            pos.z += self.speed *dt
        if keyMap["down"]:
            pos.z -= self.speed *dt
        if keyMap["rotate"]:
            self.angle += 10
            self.eve.setH(self.angle)
        if keyMap["running"]:
            self.eve.actorInterval("run", playRate=2).loop()
        if keyMap["walking"]:
            self.eve.actorInterval("walk", playRate=2).loop()
       





        self.eve.setPos(pos)
        return task.cont
        

    def spriteAnimation(self, task):
        self.camera.setPos(0, 0, 0)
        self.camera.reparentTo(render2d)
        self.setBackgroundColor(0.1,0.1,0.1,1)
        self.plane = self.loader.loadModel("Model/plane2x2")
        self.tex = self.loader.loadTexture("./assets/zombie.png")
        self.plane.setTexture(self.tex)
        self.tex.setMagfilter(SamplerState.FT_nearest)
        self.plane.setTransparency(TransparencyAttrib.MAlpha)
        self.plane.setScale(0.8)
        self.plane.reparentTo(render2d)
        self.taskMgr.add(self.update_texture, "update_texture")
    
    def update_texture(self, task):
        self.plane.setTexOffset(TextureStage.getDefault(), self.tx, 0)
        self.texture_update += 1
        if self.texture_update > 6:
            self.tx += self.tx_offset
            self.texture_update = 0
        return task.cont

    def loadAudio(self):
        music = self.loader.loadMusic("./assets/time.mp3")
        music.setLoop(True)
        music.play()
        music.setVolume(1)

    def loadImageAsPlane(self, filepath, yresolution = 600):        
        tex = self.loader.loadTexture(filepath)
        tex.setBorderColor(Vec4(0,0,0,0))
        tex.setWrapU(Texture.WMBorderColor)
        tex.setWrapV(Texture.WMBorderColor)
        cm = CardMaker(filepath + ' card')
        cm.setFrame(-tex.getOrigFileXSize(), tex.getOrigFileXSize(), -tex.getOrigFileYSize(), tex.getOrigFileYSize())
        card = NodePath(cm.generate())
        card.setTexture(tex)
        card.setScale(card.getScale()/ yresolution)
        card.flattenLight() 
        return card
    




game = MyGame()

bar = DirectWaitBar(text="", value=50, pos=(0, .4, 0), barColor=(0.203, .458, .427,1))
bar['value'] += 10
game.graphicsEngine.renderFrame() 
bar['value'] += 10
game.graphicsEngine.renderFrame() 
bar['value'] += 30
game.graphicsEngine.renderFrame()
game.graphicsEngine.renderFrame() 
bar.destroy()
game.run()

