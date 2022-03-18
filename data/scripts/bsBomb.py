import bs
import bsUtils
from bsVector import Vector
import random
import bsSpaz
import weakref


class BombFactory(object):
    """
    I deleted the description, you probably don't need them
    """

    def getRandomExplodeSound(self):
        'Return a random explosion bs.Sound from the factory.'
        return self.explodeSounds[random.randrange(len(self.explodeSounds))]

    def __init__(self):
        """
        Instantiate a BombFactory.
        You shouldn't need to do this; call bs.Bomb.getFactory() to get a
        shared instance.
        """

        self.bombModel = bs.getModel('bomb')
        self.stickyBombModel = bs.getModel('bombSticky')
        self.impactBombModel = bs.getModel('impactBomb')
        self.landMineModel = bs.getModel('landMine')
        self.tntModel = bs.getModel('tnt')
        self.knockerBombModel = bs.getModel('bomb')
        self.jumpModel = bs.getModel('impactBomb')
        self.dynamiteModel = bs.getModel('powerup')
        self.fireBombModel = bs.getModel('shockWave')
        self.curseBombModel = bs.getModel('bomb')
        self.shockWaveModel = bs.getModel('shockWave')
        self.floatModel = bs.getModel('agentHead')
        self.boxModel = bs.getModel('locatorBox')
        self.timeModel = bs.getModel('landMine')

        self.regularTex = bs.getTexture('storeCharacterEaster')
        self.iceTex = bs.getTexture('powerupIceBombs')
        self.stickyTex = bs.getTexture('aliColorMask')
        self.impactTex = bs.getTexture('fuse')
        self.impactLitTex = bs.getTexture('impactBombColorLit')
        self.landMineTex = bs.getTexture('gameCircleIcon')
        self.landMineLitTex = bs.getTexture('white')
        self.tntTex = bs.getTexture('logo')
        self.triggerTex = bs.getTexture('coin')
        self.freezeTex = bs.getTexture('ouyaUButton')
        self.clusterTex = bs.getTexture('achievementWall')        
        self.fireTex = bs.getTexture('egg4')
        self.dynamiteTex = bs.getTexture('landMine')
        self.dynamite2Tex = bs.getTexture('landMineLit')
        self.healTex = bs.getTexture('heart')
        self.curseTex = bs.getTexture('powerupCurse')
        self.shockWaveTex = bs.getTexture('levelIcon')
        self.floatTex = bs.getTexture('white')
        self.knockerTex = bs.getTexture('bg')
        self.knockerTex2 = bs.getTexture('black')
        self.boxBomb = bs.getTexture('characterIconMask')
        self.timeTex = bs.getTexture('powerupImpactBombs')
        self.elonTex = bs.getTexture('achievementCrossHair')
        self.TNTTex = bs.getTexture('tnt')
        self.noneTex = None
        
        self.hissSound = bs.getSound('hiss')
        self.debrisFallSound = bs.getSound('debrisFall')
        self.woodDebrisFallSound = bs.getSound('woodDebrisFall')

        self.explodeSounds = (bs.getSound('explosion01'),
                              bs.getSound('explosion02'),
                              bs.getSound('explosion03'),
                              bs.getSound('explosion04'),
                              bs.getSound('explosion05'))

        self.freezeSound = bs.getSound('freeze')
        self.curseSound = bs.getSound('ticking')
        self.fuseSound = bs.getSound('fuse01')
        self.activateSound = bs.getSound('activateBeep')
        self.warnSound = bs.getSound('warnBeep')

        # set up our material so new bombs dont collide with objects
        # that they are initially overlapping
        self.bombMaterial = bs.Material()
        self.normalSoundMaterial = bs.Material()
        self.stickyMaterial = bs.Material()

        self.bombMaterial.addActions(
            conditions=((('weAreYoungerThan',100),
                         'or',('theyAreYoungerThan',100)),
                        'and',('theyHaveMaterial',
                               bs.getSharedObject('objectMaterial'))),
            actions=(('modifyNodeCollision','collide',False)))

        # we want pickup materials to always hit us even if we're currently not
        # colliding with their node (generally due to the above rule)
        self.bombMaterial.addActions(
            conditions=('theyHaveMaterial',
                        bs.getSharedObject('pickupMaterial')),
            actions=(('modifyPartCollision','useNodeCollide', False)))
        
        self.bombMaterial.addActions(actions=('modifyPartCollision',
                                              'friction', 0.3))

        self.landMineNoExplodeMaterial = bs.Material()
        self.landMineBlastMaterial = bs.Material()
        self.landMineBlastMaterial.addActions(
            conditions=(
                ('weAreOlderThan',200),
                 'and', ('theyAreOlderThan',200),
                 'and', ('evalColliding',),
                 'and', (('theyDontHaveMaterial',
                          self.landMineNoExplodeMaterial),
                         'and', (('theyHaveMaterial',
                                  bs.getSharedObject('objectMaterial')),
                                 'or',('theyHaveMaterial',
                                       bs.getSharedObject('playerMaterial'))))),
            actions=(('message', 'ourNode', 'atConnect', ImpactMessage())))
        self.forseBombMaterial = bs.Material()
        self.forseBombMaterial.addActions(
            conditions=(('weAreOlderThan',200),
                        'and',('theyAreOlderThan',200),
                        'and',('evalColliding',),
                        'and',(('theyDontHaveMaterial',self.landMineNoExplodeMaterial),
                               'and',(('theyHaveMaterial',bs.getSharedObject('objectMaterial')),
                                      'or',('theyHaveMaterial',bs.getSharedObject('playerMaterial'))))),
            actions=(('message','ourNode','atConnect',StickyMessage())))

        self.impactBlastMaterial = bs.Material()
        self.impactBlastMaterial.addActions(
            conditions=(('weAreOlderThan', 200),
                        'and', ('theyAreOlderThan',200),
                        'and', ('evalColliding',),
                        'and', (('theyHaveMaterial',
                                 bs.getSharedObject('footingMaterial')),
                               'or',('theyHaveMaterial',
                                     bs.getSharedObject('objectMaterial')))),
            actions=(('message','ourNode','atConnect',ImpactMessage())))

        self.blastMaterial = bs.Material()
        self.blastMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('objectMaterial'))),
            actions=(('modifyPartCollision','collide',True),
                     ('modifyPartCollision','physical',False),
                     ('message','ourNode','atConnect',ExplodeHitMessage())))

        self.dinkSounds = (bs.getSound('bombDrop01'),
                           bs.getSound('bombDrop02'))
        self.stickyImpactSound = bs.getSound('stickyImpact')
        self.rollSound = bs.getSound('bombRoll01')

        # collision sounds
        self.normalSoundMaterial.addActions(
            conditions=('theyHaveMaterial',
                        bs.getSharedObject('footingMaterial')),
            actions=(('impactSound',self.dinkSounds,2,0.8),
                     ('rollSound',self.rollSound,3,6)))

        self.stickyMaterial.addActions(
            actions=(('modifyPartCollision','stiffness',0.1),
                     ('modifyPartCollision','damping',1.0)))

        self.stickyMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial')),
                        'or', ('theyHaveMaterial',
                               bs.getSharedObject('footingMaterial'))),
            actions=(('message','ourNode','atConnect',SplatMessage())))

class SplatMessage(object):
    pass

class ExplodeMessage(object):
    pass

class ImpactMessage(object):
    """ impact bomb touched something """
    pass

class ArmMessage(object):
    pass
class FloatMessage(object):
    pass
class WarnMessage(object):
    pass
class StickyMessage(object):
	pass
class AnimateMessage(object):
    pass
    
class ExplodeHitMessage(object):
    "Message saying an object was hit"
    def __init__(self):
        pass

class Blast(bs.Actor):
    """
    category: Game Flow Classes

    An explosion, as generated by a bs.Bomb.
    """
    def __init__(self, position=(0,1,0), velocity=(0,0,0), blastRadius=2.0,
                 blastType="normal", sourcePlayer=None, hitType='explosion',
                 hitSubType='normal'):
        """
        Instantiate with given values.
        """
        bs.Actor.__init__(self)
        
        factory = Bomb.getFactory()

        self.blastType = blastType
        self.sourcePlayer = sourcePlayer

        self.hitType = hitType;
        self.hitSubType = hitSubType;

        # blast radius
        self.radius = blastRadius

        # set our position a bit lower so we throw more things upward
        self.node = bs.newNode('region', delegate=self, attrs={
            'position':(position[0], position[1]-0.1, position[2]),
            'scale':(20,20,20) if self.blastType == 'atom' else (self.radius,self.radius,self.radius),
            'type':'sphere',
            'materials':(factory.blastMaterial,
                         bs.getSharedObject('attackMaterial'))})

        bs.gameTimer(50, self.node.delete)

        # throw in an explosion and flash
        explosion = bs.newNode("explosion", attrs={
            'position':position,
            'velocity':(velocity[0],max(-1.0,velocity[1]),velocity[2]),
            'radius':17 if self.blastType == 'grom' else self.radius,
            'big':(self.blastType in ['tnt','flash'])})
        if self.blastType in ["ice","freeze","crystal"]:
            explosion.color = (0, 0.05, 0.4)
        elif self.blastType == "knocker":
        	explosion.color = (0, 0, 2)
        elif self.blastType == "tnt":
        	explosion.color = (0, 1, 2)
        elif self.blastType == 'dynamite':
        	explosion.color = (1,0,0)
        if self.blastType == "grom":
        	explosion.color = (1000,1000,1000)
        elif self.blastType == "shockWave":
        	explosion.color = (1,0,1)
        elif self.blastType == "curse":
        	explosion.color = (0.00001,0.00001,0.00001)
        if self.blastType == "cluster":
            explosion.color = (2, 0.05, 0.4)
            self.shield = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(random.random()*2,random.random()*2,random.random()*10),'radius':3.2})
            self.node.connectAttr('position',self.shield,'position')
            self.node.handleMessage("knockout",10000)
            def platform():
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]+1,self.node.position[1]+4,self.node.position[2]),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]+2,self.node.position[1]+4,self.node.position[2]),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0],self.node.position[1]+4,self.node.position[2]),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]-1,self.node.position[1]+4,self.node.position[2]),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]-2,self.node.position[1]+4,self.node.position[2]),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]+1,self.node.position[1]+4,self.node.position[2]+1),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]+2,self.node.position[1]+4,self.node.position[2]+1),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0],self.node.position[1]+4,self.node.position[2]+1),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]-1,self.node.position[1]+4,self.node.position[2]+1),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]-2,self.node.position[1]+4,self.node.position[2]+1),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]+1,self.node.position[1]+4,self.node.position[2]),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]+2,self.node.position[1]+4,self.node.position[2]-1),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0],self.node.position[1]+4,self.node.position[2]-1),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]-1,self.node.position[1]+4,self.node.position[2]-1),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
                    trap = bs.newNode('prop', attrs={'position':(self.node.position[0]-2,self.node.position[1]+4,self.node.position[2]-1),'sticky':True,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('achievementWall'),'bodyScale':1.3,'reflection': 'powerup','density':100,'reflectionScale': [0.0],'modelScale':1.3,'gravityScale':1,'shadowSize':0.0,'materials':[bs.getSharedObject('objectMaterial')]})
                    bs.gameTimer(15000,trap.delete)
            bs.gameTimer(1,bs.Call(platform))
        elif self.blastType == "fire":
            explosion.color = (2, 1.05, 0.0)
        if self.blastType == "flash":
            bs.gameTimer(4000,explosion.delete)
        if self.blastType == "fire":
            bs.gameTimer(400000,explosion.delete)
        else:
        	bs.gameTimer(1000,explosion.delete)

        if self.blastType not in ['ice','freeze','flash','heal','crystal']:
            bs.emitBGDynamics(position=position, velocity=velocity,
                              count=int(1.0+random.random()*4),
                              emitType='tendrils',tendrilType='thinSmoke')
        bs.emitBGDynamics(
            position=position, velocity=velocity,
            count=int(4.0+random.random()*4), emitType='tendrils',
            tendrilType='ice' if self.blastType == 'ice' else 'smoke')
        bs.emitBGDynamics(
            position=position, emitType='distortion',
            spread=1.0 if self.blastType == 'tnt' else 2.0)
        
        # and emit some shrapnel..
        if self.blastType in ['ice','crystal']:
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=30, spread=2.0, scale=0.4,
                                  chunkType='ice', emitType='stickers');
            bs.gameTimer(50, _doEmit) # looks better if we delay a bit
            
        elif self.blastType == 'freeze':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0+random.random()*8),scale=17,
                                  spread=0.01,chunkType='ice',emitType='stickers');
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
            
        elif self.blastType == 'sticky':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0+random.random()*8),
                                  spread=0.7,chunkType='slime');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0+random.random()*8), scale=0.5,
                                  spread=0.7,chunkType='slime');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=15, scale=0.6, chunkType='slime',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(6.0+random.random()*12),
                                  scale=0.8, spread=1.5,chunkType='spark');
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit

        elif self.blastType == 'impact': # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0+random.random()*8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0+random.random()*8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0+random.random()*15), scale=0.8,
                                  spread=1.5, chunkType='spark');
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
        elif self.blastType == 'fire': # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=(0,5,0),
                                  count=int(400.0+random.random()*800), scale=1.98,
                                  chunkType='sweat');
                bs.emitBGDynamics(position=position, velocity=(0,5,0),
                                  count=int(800.0+random.random()*105), scale=1.2,
                                  spread=1.5, chunkType='sweat');
            bs.gameTimer(5,_doEmit) # looks better if we delay a bit

        else: # regular or land mine bomb shrapnel
            def _doEmit():
                if self.blastType != 'tnt':
                    bs.emitBGDynamics(position=position, velocity=velocity,
                                      count=int(4.0+random.random()*8),
                                      chunkType='rock');
                    bs.emitBGDynamics(position=position, velocity=velocity,
                                      count=int(4.0+random.random()*8),
                                      scale=0.5,chunkType='rock');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=30,
                                  scale=1.0 if self.blastType=='tnt' else 0.7,
                                  chunkType='spark', emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(18.0+random.random()*20),
                                  scale=1.0 if self.blastType == 'tnt' else 0.8,
                                  spread=1.5, chunkType='spark');

                # tnt throws splintery chunks
                if self.blastType == 'tnt':
                    def _emitSplinters():
                        bs.emitBGDynamics(position=position, velocity=velocity,
                                          count=int(20.0+random.random()*25),
                                          scale=0.8, spread=1.0,
                                          chunkType='rock');
                    bs.gameTimer(10,_emitSplinters)
                
                # every now and then do a sparky one
                if self.blastType == 'tnt' or random.random() < 0.1:
                    def _emitExtraSparks():
                        bs.emitBGDynamics(position=position, velocity=velocity,
                                          count=int(10.0+random.random()*20),
                                          scale=0.8, spread=1.5,
                                          chunkType='spark');
                    bs.gameTimer(20,_emitExtraSparks)
                        
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit

        if self.blastType == 'fire':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (3,2,0),
                                  'volumeIntensityScale': 850.0})
        elif self.blastType == 'curse':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (0.1,0.1,0.1),
                                  'volumeIntensityScale': 8500.0})
        elif self.blastType == 'flash':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (9.1,80.1,100.1),
                                  'radius':100,
                                  'intensityScale': 8383883892.0,
                                  'volumeIntensityScale': 850000000.0})
        elif self.blastType == 'heal':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (9.1,0.1,0.1),
                                  'volumeIntensityScale': 8500.0})
        elif self.blastType == 'grom':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (9.1,9.1,9.1),
                                  'volumeIntensityScale': 850.0})
        elif self.blastType == 'tnt2':
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (1.1,1.1,0.1),
                                  'volumeIntensityScale': 10.0})
        elif self.blastType in ['tnt','dynamite']:
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (0.1,0.98,0.1),
                                  'volumeIntensityScale': 850.0})
        else:
            light = bs.newNode('light',
                           attrs={'position':position,
                                  'color': (0.6,0.6,1.0) if self.blastType in ['ice','freeze','crystal']
                                  else (1,0.0,2.1),
                                  'volumeIntensityScale': 10.0})

        s = random.uniform(0.6,0.9)
        scorchRadius = lightRadius = self.radius
        if self.blastType == 'tnt':
            lightRadius *= 1.4
            scorchRadius *= 1.15
            s *= 3.0
        
        iScale = 1.6
        bsUtils.animate(light,"intensity", {
            0:2.0*iScale, int(s*20):0.1*iScale,
            int(s*25):0.2*iScale, int(s*50):17.0*iScale, int(s*60):5.0*iScale,
            int(s*80):4.0*iScale, int(s*200):0.6*iScale,
            int(s*2000):0.00*iScale, int(s*3000):0.0})
        bsUtils.animate(light,"radius", {
            0:lightRadius*0.2, int(s*50):lightRadius*0.55,
            int(s*100):lightRadius*0.3, int(s*300):lightRadius*0.15,
            int(s*1000):lightRadius*0.05})
        if self.blastType == 'flash':
            bs.gameTimer(6000,light.delete)
        elif blastType == 'grom':
        	bs.gameTimer(10,light.delete)
        elif blastType == 'fire':
        	bs.gameTimer(100000,light.delete)
        else:
            bs.gameTimer(int(s*3000),light.delete)

        # make a scorch that fades over time
        scorch = bs.newNode('scorch', attrs={
            'position':position,
            'size':scorchRadius*0.5,
            'big':(self.blastType == 'tnt')})
        if self.blastType == 'ice':
            scorch.color = (1,1,1.5)
        if self.blastType == 'tnt':
            scorch.color = (0,1,0.0)
        if self.blastType == 'dynamite':
        	scorch.color = (0.1,0.1,0.1)
        if self.blastType == 'shockWave':
        	scorch.color = (1,0,1)
            
        bsUtils.animate(scorch,"presence",{3000:1, 13000:0})
        bs.gameTimer(13000,scorch.delete)

        if self.blastType in ['ice','crystal','fire','freeze']:
            bs.playSound(factory.hissSound,position=light.position)
            
        p = light.position
        bs.playSound(factory.getRandomExplodeSound(),position=p)
        bs.playSound(factory.debrisFallSound,position=p)

        if self.blastType in ['curse','fire','heal','shockWave']:
            bs.shakeCamera(intensity=0)
        else:
            bs.shakeCamera(intensity=5.0 if self.blastType == 'tnt' else 1.0)

        # tnt is more epic..
        if self.blastType == 'tnt':
            bs.playSound(factory.getRandomExplodeSound(),position=p)
            def _extraBoom():
                bs.playSound(factory.getRandomExplodeSound(),position=p)
            bs.gameTimer(250,_extraBoom)
            def _extraDebrisSound():
                bs.playSound(factory.debrisFallSound,position=p)
                bs.playSound(factory.woodDebrisFallSound,position=p)
            bs.gameTimer(400,_extraDebrisSound)

    def handleMessage(self, msg):
        self._handleMessageSanityCheck()
        
        if isinstance(msg, bs.DieMessage):
            self.node.delete()

        elif isinstance(msg, ExplodeHitMessage):
            node = bs.getCollisionInfo("opposingNode")
            if node is not None and node.exists():
                t = self.node.position

                # new
                mag = 2000.0
                if self.blastType in ['ice','freeze','fly','crystal']: mag *= 0.5
                elif self.blastType == 'landMine': mag *= 2.5
                elif self.blastType == 'elon': mag *= 1.5
                elif self.blastType == 'tnt': mag *= 2.0
                elif self.blastType == 'jump': mag *= 0.8
                elif self.blastType in ['curse','heal']: mag *= 0
                elif self.blastType in ['cluster','shockWave']: mag *= 0.2
                elif self.blastType == 'knocker': mag *= 2.0
                elif self.blastType == 'flash': mag *= 0.01
                elif self.blastType == 'grom': mag *= 20
                elif self.blastType == 'atom': mag *= 2.5

                node.handleMessage(bs.HitMessage(
                    pos=t,
                    velocity=(0,0,0),
                    magnitude=mag,
                    hitType=self.hitType,
                    hitSubType=self.hitSubType,
                    radius=self.radius,
                    sourcePlayer=self.sourcePlayer))
                if self.blastType == 'heal':
                	node.handleMessage(bs.PowerupMessage("health"))
                if self.blastType == 'shockWave':
                	node.handleMessage("knockout",5000)
                if self.blastType == 'fire':
                	node.handleMessage(bs.FireMessage())
                	bs.Napalm(position = self.node.position)
                if self.blastType == 'curse':
                	bs.playSound(Bomb.getFactory().curseSound, 10, position=t)
                	node.handleMessage(bs.PowerupMessage("curse"))
                if self.blastType == 'flash':
                    node.handleMessage("knockout",3000)
                if self.blastType == 'shockWave':
                	node.handleMessage("knockout",5000)
                if self.blastType == 'jump':
                    node.handleMessage("stand", msg.position[0], msg.position[1], msg.position[2], msg.angle)
                if self.blastType in ['ice','freeze','crystal']:
                    bs.playSound(Bomb.getFactory().freezeSound, 10, position=t)
                    node.handleMessage(bs.FreezeMessage())

        else:
            bs.Actor.handleMessage(self, msg)

class Bomb(bs.Actor):
    """
    category: Game Flow Classes
    
    A bomb and its variants such as land-mines and tnt-boxes.
    """

    def __init__(self, position=(0,1,0), velocity=(0,0,0), bombType='normal',
                 blastRadius=2.0, sourcePlayer=None, owner=None):
        """
        Create a new Bomb.
        
        bombType can be 'ice','impact','landMine','normal','sticky', or 'tnt'.
        Note that for impact or landMine bombs you have to call arm()
        before they will go off.
        """
        bs.Actor.__init__(self)
        self.aim = None

        factory = self.getFactory()

        if not bombType in ('ice','impact','atom','force2','elon','landMine','box','freeze','grom','tnt2','flash','fly','time','float','curse','backflip','shockWave','force','cluster','crystal','dynamite','knocker','heal','jump','fire','normal','noah','sticky','tnt'):
            raise Exception("invalid bomb type: " + bombType)
        self.bombType = bombType

        self._exploded = False

        if self.bombType == 'sticky': 
            self._lastStickySoundTime = 0
            name = "sticky"

        self.blastRadius = blastRadius
        if self.bombType == 'ice': 
            self.blastRadius *= 1.2
            name = "ice"
        elif self.bombType == 'impact': 
            self.blastRadius *= 0.7
            name = "impact"
        elif self.bombType == 'landMine': 
            self.blastRadius *= 0.7
            name = "landMine"
        elif self.bombType == 'tnt': 
            self.blastRadius *= 1.45
            name = "TNT"
        elif self.bombType == 'fire': 
            self.blastRadius *= 1.1
            name = "fire"
        elif self.bombType == 'freeze': 
            self.blastRadius *= 1.2
            name = "freeze"
        elif self.bombType == 'curse': 
            self.blastRadius *= 1.2
            name = "curse"
        elif self.bombType == 'noah': 
            self.blastRadius *= 1.0
            name = "noah"
        elif self.bombType == 'dynamite': 
            self.blastRadius *= 1.3
            name = "dynamite"
        elif self.bombType == 'jump': 
            self.blastRadius *= 1.0
            name = "jump"
        elif self.bombType == 'knocker': 
            self.blastRadius *= 1.5
            name = "knocker"
        elif self.bombType == 'heal': 
            self.blastRadius *= 0.8
            name = "heal"
        elif self.bombType == 'cluster': 
            self.blastRadius *= 0.8
            name = "cluster"
        elif self.bombType == 'crystal': 
            self.blastRadius *= 0.8
            name = "crystal"
        elif self.bombType in ['force','force2']: 
            self.blastRadius *= 0.8
            name = "force"
        elif self.bombType == 'shockWave': 
            self.blastRadius *= 1.4
            name = "shockWave"
        elif self.bombType == 'backflip': 
            self.blastRadius *= 0.5
            name = "backflip"
        elif self.bombType == 'flash': 
            self.blastRadius *= 1.1
            name = "flash"
        elif self.bombType == 'fly': 
            self.blastRadius *= 1.0
            name = "fly"
        elif self.bombType == 'float': 
            self.blastRadius *= 0.0
            name = "float"
        elif self.bombType == 'box': 
            self.blastRadius *= 0.9
            name = "box"
        elif self.bombType == 'tnt2': 
            self.blastRadius *= 1.45
            name = "TNT"
        elif self.bombType == 'time': 
            self.blastRadius *= 1.0 # i call this bomb time, because it will need time for explode
            name = "time"
        elif self.bombType == 'grom': 
            self.blastRadius *= 1
            name = "grom"
        elif self.bombType == 'elon': 
            self.blastRadius *= 0.7
            name = "elon"
        elif self.bombType == 'atom': 
            self.blastRadius *= 2.7
            name = "atom"

        self._explodeCallbacks = []
        
        # the player this came from
        self.sourcePlayer = sourcePlayer

        # by default our hit type/subtype is our own, but we pick up types of
        # whoever sets us off so we know what caused a chain reaction
        self.hitType = 'explosion'
        self.hitSubType = self.bombType

        # if no owner was provided, use an unconnected node ref
        if owner is None: owner = bs.Node(None)

        # the node this came from
        self.owner = owner

        # adding footing-materials to things can screw up jumping and flying
        # since players carrying those things
        # and thus touching footing objects will think they're on solid ground..
        # perhaps we don't wanna add this even in the tnt case?..
        if self.bombType in ['tnt','tnt2']:
            materials = (factory.bombMaterial,
                         bs.getSharedObject('footingMaterial'),
                         bs.getSharedObject('objectMaterial'))
        else:
            materials = (factory.bombMaterial,
                         bs.getSharedObject('objectMaterial'))
            
        if self.bombType in ['impact','force2','noah','curse','heal','crystal','shockWave']:
            materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType in ['landMine','elon']:
            materials = materials + (factory.landMineNoExplodeMaterial,)
        if self.bombType == ['sticky','time']:
            materials = materials + (factory.stickyMaterial,)
        else:
            materials = materials + (factory.normalSoundMaterial,)

        if self.bombType == 'landMine':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'model':factory.landMineModel,
                'lightModel':factory.landMineModel,
                'body':'landMine',
                'shadowSize':0.44,
                'colorTexture':factory.landMineTex,
                'reflection':'powerup',
                'reflectionScale':[1.0],
                'materials':materials})
                
        elif self.bombType == 'elon':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'model':factory.landMineModel,
                'lightModel':factory.landMineModel,
                'body':'landMine',
                'shadowSize':0.44,
                'colorTexture':factory.elonTex,
                'reflection':'powerup',
                'reflectionScale':[1.0],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': 'tracker',
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)
                
        elif self.bombType == 'float':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':(position[0], position[1]+0.1, position[2]),
                'velocity':(0,0,0),
                'model':factory.floatModel,
                'body':'crate',
                'bodyScale':1,
                'modelScale':1,
                'shadowSize':0.44,
                'colorTexture':factory.floatTex,
                'reflection':'powerup',
                'gravityScale':-5,
                'reflectionScale':[1.0],
                'materials':materials})
            self.animateTimer = bs.Timer(1,bs.WeakCall(self.handleMessage,FloatMessage()))
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)
            
        
        elif self.bombType == 'tnt':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'model':factory.tntModel,
                'lightModel':factory.tntModel,
                'body':'crate',
                'shadowSize':0.5,
                'colorTexture':factory.tntTex,
                'reflection':'soft',
                'reflectionScale':[0.23],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':1.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, False)
                
        elif self.bombType == 'tnt2':
            self.node = bs.newNode('bomb', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'model':factory.tntModel,
                'lightModel':factory.tntModel,
                'body':'crate',
                'shadowSize':0.5,
                'colorTexture':factory.TNTTex,
                'reflection':'soft',
                'reflectionScale':[0.23],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)            
            
        elif self.bombType == 'noah':
            fuseTime = 20000
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'body':'sphere', 
                                          'shadowSize':0.3,  
                                          'reflection':'powerup',
                                          'reflectionScale':[2.5],                                   
                                          'materials':materials})
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(0,0,2.7),'radius':0.7})
            self.node.connectAttr('position',self.shield1,'position')
            self.shield2 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(0,2,3),'radius':0.9})
            self.shield3 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(20,0,0),'radius':0.6})
            self.node.connectAttr('position',self.shield2,'position')
            self.node.connectAttr('position',self.shield3,'position')
            
            bs.animate(self.shield2,'radius',{0:0.1,100:0.5,600:0.1},True)         
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)                                    
        elif self.bombType == 'heal':
            fuseTime = 20000
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'body':'sphere', 
                                          'shadowSize':0.3,  
                                          'reflection':'powerup',
                                          'reflectionScale':[2.5],                                   
                                          'materials':materials})
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(2,0,0.0),'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')
            self.shield2 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(0.1,0.1,0.1),'radius':0.9})
            self.shield3 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(20,0,0),'radius':0.6})
            self.node.connectAttr('position',self.shield2,'position')
            self.node.connectAttr('position',self.shield3,'position')
            
            bs.animate(self.shield2,'radius',{0:0.1,100:0.5,600:0.5},True)         
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)
        elif self.bombType == 'flash':
            fuseTime = 2000
            self.node = bs.newNode('bomb',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'body':'sphere', 
                                          'shadowSize':0.3,  
                                          'reflection':'powerup',
                                          'reflectionScale':[2.5],                                   
                                          'materials':materials})
            bsUtils.animate(self.node, 'fuseLength', {0:1, fuseTime:0.0})
            flash = bs.newNode("flash",
                                   attrs={'position':self.node.position,
                                          'size':0.4,
                                          'color':(0,0.5,1)})
            bs.gameTimer(0, flash.delete)
            self.node.connectAttr('position',flash,'position')
            bs.animate(flash,'size',{0:0.4,1000:0.4,4000:0.4,5000:0.2,6000:1.5})  
            bs.animateArray(flash,'color',3,{0:(0.4,2,3),1000:(1.0,1.0,9.0),4000:(0.4,0.4,0.4),5000:(0.0,0.0,1.0),6000:(2,0,0)})  
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(0,0,2.2),'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')
        elif self.bombType == 'impact':
            fuseTime = 20000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'model':factory.impactBombModel,
                'shadowSize':0.3,
                'colorTexture':factory.impactTex,
                'reflection':'powerup',
                'reflectionScale':[1.5],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)
        elif self.bombType == 'time':
            fuseTime = 10000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'landMine',
                'owner':owner,
                'model':factory.timeModel,
                'shadowSize':0.3,
                'sticky':True,
                'colorTexture':factory.timeTex,
                'reflection':'sharper',
                'reflectionScale':[1.5],
                'materials':materials})
        elif self.bombType == 'box':
            fuseTime = 3000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'model':factory.boxModel,
                'shadowSize':0.3,
                'colorTexture':factory.boxBomb,
                'reflection':'powerup',
                'reflectionScale':[1.5],
                'materials':materials})    
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)
        elif self.bombType == 'crystal':
            fuseTime = 999999
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'model':factory.impactBombModel,
                'shadowSize':0.3,
                'colorTexture':factory.iceTex,
                'reflection':'soft',
                'reflectionScale':[3.5],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)
        elif self.bombType == 'curse':
            fuseTime = 50000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'model':factory.curseBombModel,
                'shadowSize':0.3,
                'colorTexture':factory.curseTex,
                'reflection':'powerup',
                'reflectionScale':[1.5],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)
        elif self.bombType == 'shockWave':
            fuseTime = 9999289299390
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'model':factory.shockWaveModel,
                'shadowSize':0.3,
                'modelScale':0.02,
                'colorTexture':factory.shockWaveTex,
                'reflection':'sharp',
                'reflectionScale':[1.5],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)
        elif self.bombType == 'jump':
            fuseTime = 1
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'shadowSize':0.3,
                'reflection':'powerup',
                'reflectionScale':[1.5],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)            
        elif self.bombType == 'backflip':
            fuseTime = 1
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'shadowSize':0.3,
                'reflection':'powerup',
                'reflectionScale':[1.5],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)            
        elif self.bombType == 'grom':
            fuseTime = 3150
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'model':bs.getModel('bomb'),
                'shadowSize':0.3,
                'colorTexture':bs.getTexture('scorch'),
                'reflection':'powerup',
                'reflectionScale':[1.5],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)            
        elif self.bombType == 'force2':
            fuseTime = 3150
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'model':bs.getModel('bombSticky'),
                'shadowSize':0.3,
                'colorTexture':bs.getTexture('touchArrowsActions'),
                'reflection':'sharper',
                'reflectionScale':[1.5],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)            
        elif self.bombType == 'dynamite':
            fuseTime = 3100
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'model':factory.dynamiteModel,
                'shadowSize':0.3,
                'colorTexture':factory.dynamiteTex,
                'reflection':'powerup',
                'reflectionScale':[1.5],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.8})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': 'dynamite',
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)           
            self.animateTimer = bs.Timer(1,bs.WeakCall(self.handleMessage,AnimateMessage()))
            self.warnTimer = bs.Timer(fuseTime-100,
                                      bs.WeakCall(self.handleMessage,
                                                  WarnMessage()))
            self.armTimer = bs.Timer(200, bs.WeakCall(self.handleMessage,
                                                      ArmMessage()))
        else:
            fuseTime = 3000
            if self.bombType in ['sticky','freeze','force2']:
                sticky = True
                model = factory.stickyBombModel
                rType = 'sharper'
                rScale = 1.8
                bScale = 1
            elif self.bombType == 'fire':
                sticky = False
                model = factory.fireBombModel
                rType = 'sharper'
                rScale = 1.8
            elif self.bombType == 'fly':
                sticky = False
                model = factory.bombModel
                rType = 'sharper'
                rScale = 100.8
            elif self.bombType == 'knocker':
                sticky = False
                model = factory.knockerBombModel
                rType = 'soft'
                rScale = 2.8
                self.animateTimer = bs.Timer(1,bs.WeakCall(self.handleMessage,AnimateMessage()))
            elif self.bombType == 'atom':
                sticky = False
                model = bs.getModel('powerup')
                rType = 'soft'
                rScale = 1.8
            else:
                sticky = False
                model = factory.bombModel
                rType = 'sharper'
                rScale = 1.8
                bScale = 1
            if self.bombType == 'ice': tex = factory.iceTex
            elif self.bombType == 'sticky': tex = factory.stickyTex
            elif self.bombType == 'fire': tex = factory.fireTex
            elif self.bombType in ['knocker','fly']: tex = factory.knockerTex
            elif self.bombType == 'cluster': tex = factory.clusterTex
            elif self.bombType == 'grom': tex = bs.getTexture('scorch')
            elif self.bombType in ['freeze']: tex = factory.freezeTex
            elif self.bombType in ['force']: tex = bs.getTexture('touchArrowsActions')
            else: tex = factory.regularTex
            self.node = bs.newNode('bomb', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'model':model,
                'shadowSize':0.3,
                'colorTexture':tex,
                'sticky':sticky,
                'owner':owner,
                'reflection':rType,
                'reflectionScale':[rScale],
                'materials':materials})
            prefixAnim = {0: (2, 0, 0), 250: (2, 2, 0), 250 * 2: (0, 2, 0), 250 * 3: (0, 2, 2), 250 * 4: (2, 0, 2),
                      250 * 5: (0, 0, 2), 250 * 6: (2, 0, 0)}
            color = (random.random(), random.random(), random.random())
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':color,'radius':0.7})
            self.node.connectAttr('position',self.shield1,'position')  
            bsUtils.animateArray(self.shield1, 'color', 3, prefixAnim, True)
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(self.bombType),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)            

            sound = bs.newNode('sound', owner=self.node, attrs={
                'sound':factory.fuseSound,
                'volume':0.25})
            self.node.connectAttr('position', sound, 'position')
            if self.bombType == 'fire':
                bsUtils.animate(self.node, 'fuseLength', {0:0, fuseTime:0.0})
            if self.bombType == 'flash':
                bsUtils.animate(self.node, 'fuseLength', {0:1, fuseTime:0.0})
            else:
            	bsUtils.animate(self.node, 'fuseLength', {0:1.0, fuseTime:0.0})

        # light the fuse!!!
        if self.bombType not in ('landMine','elon','tnt','force2','shockWave','tnt2','curse','float'):
            bs.gameTimer(fuseTime,
                         bs.WeakCall(self.handleMessage, ExplodeMessage()))
        if self.bombType == 'shockWave':
        	bsUtils.animate(self.node,"modelScale",{0:0, 200:0.5, 260:0.3})
        elif self.bombType == 'fire':
        	bsUtils.animate(self.node,"modelScale",{0:0, 200:0.3, 260:0.3})
        else:
            bsUtils.animate(self.node,"modelScale",{0:0, 200:1.3, 260:1})

    def getSourcePlayer(self):
        """
        Returns a bs.Player representing the source of this bomb.
        """
        if self.sourcePlayer is None: return bs.Player(None) # empty player ref
        return self.sourcePlayer
        
    @classmethod
    def getFactory(cls):
        """
        Returns a shared bs.BombFactory object, creating it if necessary.
        """
        activity = bs.getActivity()
        try: return activity._sharedBombFactory
        except Exception:
            f = activity._sharedBombFactory = BombFactory()
            return f

    def onFinalize(self):
        bs.Actor.onFinalize(self)
        # release callbacks/refs so we don't wind up with dependency loops..
        self._explodeCallbacks = []
        
    def _handleDie(self,m):
        self.node.delete()
        
    def _handleOOB(self, msg):
        self.handleMessage(bs.DieMessage())

    def _handleImpact(self,m):
        node,body = bs.getCollisionInfo("opposingNode","opposingBody")
        # if we're an impact bomb and we came from this node, don't explode...
        # alternately if we're hitting another impact-bomb from the same source,
        # don't explode...
        try: nodeDelegate = node.getDelegate()
        except Exception: nodeDelegate = None
        if node is not None and node.exists():
            if (self.bombType in ['impact','noah','curse','heal','fire','crystal','shockWave'] and
                (node is self.owner
                 or (isinstance(nodeDelegate, Bomb)
                     and nodeDelegate.bombType in ['impact','noah','curse','fire','heal','crystal','shockWave']
                     and nodeDelegate.owner is self.owner))): return
            else:
                self.handleMessage(ExplodeMessage())

    def float(self):
    	if self.bombType == 'float':
		    oldY = self.node.extraAcceleration[0]
		    newY = {0: 0, 1: 309, 2: 109 + 200 * 2, 3: 109 + 200 * 3}.get(self.heldBy, 0) # needs more science
		    time = 30 if (oldY >= newY) else 100
		    keys = {0: (0, oldY, 0), time: (0, newY, 0)}
		    bs.animateArray(self.node, 'extraAcceleration', 3, keys)

    def _handleDropped(self,m):
        if self.bombType in ['landMine']:
            self.armTimer = \
                bs.Timer(1250, bs.WeakCall(self.handleMessage, ArmMessage()))
        elif self.bombType in ['force','elon','force2']:
            self.armTimer = bs.Timer(250,bs.WeakCall(self.handleMessage,ArmMessage()))
            self.Timer = bs.Timer(250,bs.WeakCall(self.handleMessage,ImpactMessage()))
        elif self.bombType == 'dynamite':
            self.armTimer = \
                bs.Timer(1700, bs.WeakCall(self.handleMessage, ArmMessage()))
        # once we've thrown a sticky bomb we can stick to it..
        elif self.bombType in ['sticky','time']:
            def _safeSetAttr(node,attr,value):
                if node.exists(): setattr(node,attr,value)
            bs.gameTimer(
                2500, lambda: _safeSetAttr(self.node, 'stickToOwner', True))
    
    def _handleSplat(self,m):
        node = bs.getCollisionInfo("opposingNode")
        if (node is not self.owner
                and bs.getGameTime() - self._lastStickySoundTime > 1000):
            self._lastStickySoundTime = bs.getGameTime()
            bs.playSound(self.getFactory().stickyImpactSound, 2.0,
                         position=self.node.position)

    def addExplodeCallback(self,call):
        """
        Add a call to be run when the bomb has exploded.
        The bomb and the new blast object are passed as arguments.
        """
        self._explodeCallbacks.append(call)
    
    def explode(self):
        """
        Blows up the bomb if it has not yet done so.
        """
        
        if self._exploded: return
        self._exploded = True
        activity = self.getActivity()
        if self.bombType == 'shockWave':
        	material.ShockWave(position = self.node.position)
        elif self.bombType == 'fire':
            material.Napalm(position = self.node.position)
        elif self.bombType == 'flash':
            material.Flash(position = self.node.position)
        elif self.bombType in ['jump','backflip']:
            blast = Blast(position=(self.node.position[0],self.node.position[1]-1.15,self.node.position[2]),velocity=self.node.velocity,
                            blastRadius=self.blastRadius,blastType=self.bombType,sourcePlayer=self.sourcePlayer,hitType=self.bombType,hitSubType=self.hitSubType).autoRetain()
            for c in self._explodeCallbacks: c(self,blast)
        if activity is not None and self.node.exists():
            blast = Blast(
                position=self.node.position,
                velocity=self.node.velocity,
                blastRadius=self.blastRadius,
                blastType=self.bombType,
                sourcePlayer=self.sourcePlayer,
                hitType=self.hitType,
                hitSubType=self.hitSubType).autoRetain()
            for c in self._explodeCallbacks: c(self,blast)
        # we blew up so we need to go away
        bs.gameTimer(1, bs.WeakCall(self.handleMessage, bs.DieMessage()))

    def _handleWarn(self, m):
        if self.textureSequence.exists():
            self.textureSequence.rate = 30
            bs.playSound(self.getFactory().warnSound, 0.5,
                         position=self.node.position)

    def _addMaterial(self, material):
        if not self.node.exists(): return
        materials = self.node.materials
        if not material in materials:
            self.node.materials = materials + (material,)
    
    def arm(self):
        """
        Arms land-mines and impact-bombs so
        that they will explode on impact.
        """
        if not self.node.exists(): return
        factory = self.getFactory()
        if self.bombType == 'dynamite':
            self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate':30,
                    'inputTextures':(factory.dynamiteTex2,
                                     factory.dynamiteTex)})
            bs.gameTimer(500,self.textureSequence.delete)
            # we now make it explodable.
            bs.gameTimer(250,bs.WeakCall(self._addMaterial,
                                         factory.landMineBlastMaterial))
        elif self.bombType in ['force','force2']:
            #self.setSticky()
            bs.playSound(bs.getSound('activateBeep'),position = self.node.position)
            self.aim = material.AutoAim(self.node,self.owner)
            self.handleMessage(bs.ImpactMessage())
        elif self.bombType == 'landMine':
            self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate':30,
                    'inputTextures':(factory.landMineLitTex,
                                     factory.landMineTex)})
            bs.gameTimer(500,self.textureSequence.delete)
            # we now make it explodable.
            bs.gameTimer(250,bs.WeakCall(self._addMaterial,
                                         factory.landMineBlastMaterial))
        elif self.bombType == 'elon':
            self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate':30,
                    'inputTextures':(factory.landMineLitTex,
                                     factory.elonTex)})
            bs.gameTimer(500,self.textureSequence.delete)
            bs.gameTimer(250,bs.WeakCall(self._addMaterial,
                                         factory.landMineBlastMaterial))
            bs.playSound(bs.getSound('activateBeep'),position = self.node.position)
            self.aim = material.AutoAim(self.node,self.owner)
        elif self.bombType == 'impact':
            self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate':100,
                    'inputTextures':(factory.impactLitTex,
                                     factory.impactTex,
                                     factory.impactTex)})
            bs.gameTimer(250, bs.WeakCall(self._addMaterial,
                                          factory.landMineBlastMaterial))
        else:
            raise Exception('arm() should only be called '
                            'on land-mines or impact bombs')
        self.textureSequence.connectAttr('outputTexture',
                                         self.node, 'colorTexture')
        bs.playSound(factory.activateSound, 0.5, position=self.node.position)
        
    def animate(self):
    	if not self.node.exists(): return
        factory = self.getFactory()
        if self.bombType == 'knocker':
        	bsUtils.animate(self.node, 'modelScale', {0:0, 100:1,  1000:1.1, 2000:1, 3000:1.25})
        if self.bombType == 'dynamite':
            def dynamiteAnim():
                try:
                    if self.node.colorTexture == factory.dynamiteTex:
                        self.node.colorTexture = factory.dynamite2Tex
                    elif self.node.colorTexture == factory.dynamite2Tex:
                        self.node.colorTexture = factory.dynamiteTex
                except:
                    def shit(): pass
                    self.dynamiteAnim = bs.Timer(1,shit,True)
            self.dynamiteAnim = bs.Timer(150,dynamiteAnim,True)
            
    def _handleHit(self, msg):
        isPunch = (msg.srcNode.exists() and msg.srcNode.getNodeType() == 'spaz')

        # normal bombs are triggered by non-punch impacts..
        # impact-bombs by all impacts
        if (not isPunch or self.bombType == 'tnt2'):
        	bs.gameTimer(3000+int(random.random()*1000),
                         bs.WeakCall(self.handleMessage, ExplodeMessage()))
        if (not self._exploded and not isPunch
            or self.bombType in ['impact','time','landMine','force2','crystal']):
            # also lets change the owner of the bomb to whoever is setting
            # us off.. (this way points for big chain reactions go to the
            # person causing them)
            if msg.sourcePlayer not in [None]:
                self.sourcePlayer = msg.sourcePlayer

                # also inherit the hit type (if a landmine sets off by a bomb,
                # the credit should go to the mine)
                # the exception is TNT.  TNT always gets credit.
                if self.bombType not in ['tnt','curse','knocker','heal','shockWave']:
                    self.hitType = msg.hitType
                    self.hitSubType = msg.hitSubType
            if msg.hitSubType not in ['curse','jump','knocker','heal','cluster','shockWave']:
                if self.bombType not in ['knocker','curse','heal']:
                    bs.gameTimer(100+int(random.random()*100),
                         bs.WeakCall(self.handleMessage, ExplodeMessage()))
        self.node.handleMessage(
            "impulse", msg.pos[0], msg.pos[1], msg.pos[2],
            msg.velocity[0], msg.velocity[1], msg.velocity[2],
            msg.magnitude, msg.velocityMagnitude, msg.radius, 0,
            msg.velocity[0], msg.velocity[1], msg.velocity[2])

        if msg.srcNode.exists():
            pass
        
    def handleMessage(self, msg):
        if isinstance(msg, ExplodeMessage): self.explode()
        elif isinstance(msg, ImpactMessage):
           if not self.bombType in ['force','force2']:
               self._handleImpact(msg)
           elif self.bombType in ['force','force2']:
           	self._handleForceBomb(msg)
        elif isinstance(msg, bs.PickedUpMessage):
            # change our source to whoever just picked us up *only* if its None
            # this way we can get points for killing bots with their own bombs
            # hmm would there be a downside to this?...
            if self.sourcePlayer is not None:
                self.sourcePlayer = msg.node.sourcePlayer
        elif isinstance(msg, SplatMessage): self._handleSplat(msg)
        elif isinstance(msg, bs.DroppedMessage): self._handleDropped(msg)
        elif isinstance(msg, bs.HitMessage): self._handleHit(msg)
        elif isinstance(msg, bs.DieMessage): self._handleDie(msg)
        elif isinstance(msg, bs.OutOfBoundsMessage): self._handleOOB(msg)
        elif isinstance(msg, ArmMessage): self.arm()
        elif isinstance(msg, WarnMessage): self._handleWarn(msg)
        elif isinstance(msg, StickyMessage): self.node.sticky = True
        elif isinstance(msg,AnimateMessage): self.animate()
        elif isinstance(msg,FloatMessage): self.float()
        else: bs.Actor.handleMessage(self, msg)

class TNTSpawner(object):
    """
    category: Game Flow Classes

    Regenerates TNT at a given point in space every now and then.
    """
    def __init__(self,position,respawnTime=30000):
        """
        Instantiate with a given position and respawnTime (in milliseconds).
        """
        self._position = position
        self._tnt = None
        self._update()
        self._updateTimer = bs.Timer(1000,bs.WeakCall(self._update),repeat=True)
        self._respawnTime = int(random.uniform(0.8,1.2)*respawnTime)
        self._waitTime = 0
        
    def _update(self):
        tntAlive = self._tnt is not None and self._tnt.node.exists()
        if not tntAlive:
            # respawn if its been long enough.. otherwise just increment our
            # how-long-since-we-died value
            if self._tnt is None or self._waitTime >= self._respawnTime:
                self._tnt = Bomb(position=self._position,bombType='tnt')
                self._waitTime = 0
            else: self._waitTime += 1000
