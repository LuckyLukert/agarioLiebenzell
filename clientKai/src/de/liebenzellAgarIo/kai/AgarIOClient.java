package de.liebenzellAgarIo.kai;

import javax.swing.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.util.*;

public class AgarIOClient extends JFrame implements MouseMotionListener,NetworkInterface,Runnable,KeyListener{
	private World world;
	private NetworkCommunication nI;
	private int id;
	private DrawPanel dp;
	
	private Thread thread;
	private boolean run=false;
	
	private long lastMove;
	private boolean keyPressed = false;
	
	public static final int SCREEN_X=700;
	public static final int SCREEN_Y=700;
	
	public static final int PLAYER_SIZE = 50;
	
	public static final double SCALE = 1;
	
	public BufferedImage current,buffer;
	
	public AgarIOClient() {
		super("MyAgarIoClient");
		
		nI = new NetworkCommunication(JOptionPane.showInputDialog("Name:"),JOptionPane.showInputDialog("IP"),this);
//		nI = new NetworkCommunication("stirbCherryWorm","192.168.1.169",this);
		dp = new DrawPanel();
		
		setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
		setResizable(false);
		
		add(dp);
		pack();
		setVisible(true);
		
		current = new BufferedImage(SCREEN_X, SCREEN_Y,BufferedImage.TYPE_INT_RGB);
		buffer = new BufferedImage(SCREEN_X, SCREEN_Y,BufferedImage.TYPE_INT_RGB);
		
		
		addKeyListener(this);
		addMouseMotionListener(this);
		
	}
	
	private void gameOver() {
		run = false;
		System.exit(0);
	}
	
	private void startGame() {
		run = true;
		thread = new Thread(this);
		thread.start();
	}

	@Override
	public void join(World world, int id) {
		this.world = world;
		this.id = id;
		
		System.out.println("Joined");
		
		startGame();
	}

	@Override
	public void joinWatcher(World world) {
		//TODO not supported yet
	}

	@Override
	public void playerJoined(int id, Player player) {
		if(run) {
			synchronized(world.players) {
				world.players.put(id, player);
			}
		}
	}

	@Override
	public void playerKilled(int id) {
		if(run) {
			synchronized (world.players) {
				world.players.remove(id);				
			}
			
			if(id == this.id) {
				System.exit(0);
				gameOver();
			}
		}
	}

	@Override
	public void playerMoves(int id,LinkedList<Ball> balls) {
		if(run){
			synchronized (world.players) {
//				System.out.println(id);
				if(world.players.containsKey(id)){world.players.get(id).balls = balls;}
			}
		}
	}

	@Override
	public void obstacleAdd(int id, Ball ball) {
		if(run) {
			synchronized (world.obstacles) {
				world.obstacles.put(id, ball);	
			}
		}
	}

	@Override
	public void obstacleRemove(int id) {
		if(run) {
			synchronized (world.obstacles) {
				world.obstacles.remove(id);	
			}
		}
	}

	@Override
	public void foodAdd(int id, Ball ball) {
		if(run) {
			synchronized (world.food) {
				world.food.put(id, ball);	
			}
		}
	}

	@Override
	public void foodRemove(int id) {
		if(run) {
			synchronized (world.food) {
				world.food.remove(id);	
			}
		}
	}

	@Override
	public void foodMove(int id, Ball ball) {
		if(run) {
			synchronized (world.food) {
				world.food.put(id, ball);	
			}
		}
	}

	@Override
	public void mouseDragged(MouseEvent arg0) {}

	@Override
	public void mouseMoved(MouseEvent arg0) {
		long t = System.currentTimeMillis();
		if(t-lastMove<50) {
			return;
		}
		lastMove = t;
		
		int x = arg0.getX();
		int y = arg0.getY();
		
		int cX = SCREEN_Y/2;
		int cY = SCREEN_Y/2;
		
		int dx = (x - cX)/25;		
		int dy = (y - cY)/25;
		
		nI.move(new Vector(dx, dy));
	}
	
	public void run() {
		int dt;
		long lastT = System.currentTimeMillis();
		
		while(run) {

			Graphics2D g = (Graphics2D) buffer.getGraphics();
			synchronized (world) {
				
				long cT = System.currentTimeMillis();
				dt = (int) (cT-lastT);
				
				Player self = world.players.get(id);
				Point sPos = self.balls.peekFirst().pos;
				
//				synchronized(world.players){
//					for(Ball b:self.balls) {
////						moveBall(dt,b);
//					}
//				}
				
				int size=0;
				for(Ball b:self.balls) {
					size+= b.size;
				}
				
//				double scale = ((double) size)/size; //TODO scale
//				g.scale(scale, scale);
				
				int xShift = (int) (sPos.x-SCREEN_X/2);
				int yShift = (int) (sPos.y-SCREEN_Y/2);
				
				
				
				
				//draw food
				synchronized (world.food) {
					Set<Integer> s = world.food.keySet();

					g.setColor(Color.BLACK);
					g.fillRect(0, 0, SCREEN_X, SCREEN_Y);
					 RenderingHints rh = new RenderingHints(
				             RenderingHints.KEY_TEXT_ANTIALIASING,
				             RenderingHints.VALUE_TEXT_ANTIALIAS_OFF);
				    g.setRenderingHints(rh);
					for(Integer i:s) {
						Ball b = world.food.get(i);
						String c = b.color.substring(1, b.color.length());
						g.setColor(new Color(Integer.valueOf(c,16)));
//						moveBall(dt,b);
						g.fillOval((int) (SCALE*(b.pos.x-xShift-b.size)),(int) (SCALE*(b.pos.y-yShift-b.size)),(int)( SCALE*2*b.size),(int) (SCALE*2*b.size));
						g.setColor(g.getColor().brighter().brighter());
						g.drawOval((int) (SCALE*(b.pos.x-xShift-b.size)),(int) (SCALE*(b.pos.y-yShift-b.size)),(int)( SCALE*2*b.size),(int) (SCALE*2*b.size));
					}
				}
				
				
				synchronized (world.obstacles) {
					//draw obstacles
					Set<Integer> s = world.obstacles.keySet();
					for(Integer i:s) {
						Ball b = world.obstacles.get(i);
						String c = b.color.substring(1, b.color.length());
						g.setColor(new Color(Integer.valueOf(c,16)));
//						moveBall(dt,b);
						g.fillOval((int) (SCALE*(b.pos.x-xShift-b.size)),(int) (SCALE*(b.pos.y-yShift-b.size)),(int)( SCALE*2*b.size),(int) (SCALE*2*b.size));
						g.setColor(g.getColor().brighter().brighter());;
						g.drawOval((int) (SCALE*(b.pos.x-xShift-b.size)),(int) (SCALE*(b.pos.y-yShift-b.size)),(int)( SCALE*2*b.size),(int) (SCALE*2*b.size));
					}
				}
				
				
				
				g.setColor(Color.RED);
				//draw player
				synchronized(world.players) {
					Set<Integer> s = world.players.keySet();
					for(Integer i:s) {
						Player p = world.players.get(i);
						for(Ball b:p.balls) {
							String c = b.color.substring(1, b.color.length());
							g.setColor(new Color(Integer.valueOf(c,16)));
//							if(i!=id) {moveBall(dt,b);}
							g.fillOval((int) (SCALE*(b.pos.x-xShift-b.size)),(int) (SCALE*(b.pos.y-yShift-b.size)),(int)( SCALE*2*b.size),(int) (SCALE*2*b.size));
							g.setColor(g.getColor().brighter().brighter());;
							g.drawOval((int) (SCALE*(b.pos.x-xShift-b.size)),(int) (SCALE*(b.pos.y-yShift-b.size)),(int)( SCALE*2*b.size),(int) (SCALE*2*b.size));
						}
						Point pos = p.balls.peekFirst().pos;
						g.setColor(Color.WHITE);
						g.drawString(p.name,(int) (SCALE*(pos.x-xShift)),(int) (SCALE*(pos.y-yShift)));
					}
				}
				
				
				
			}
			
			g.dispose();
			
			Graphics g2 = dp.getGraphics();
			g2.drawImage(buffer, 0, 0, null);
			BufferedImage tmp = current;
			current = buffer;
			buffer = tmp;
			
			
			try {
				Thread.sleep(40);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}		
			
		}
	}

	private void moveBall(int dt, Ball b) {
		b.pos.x = (int) (b.pos.x+(dt/10.0)*b.speed.x);
		b.pos.y = (int) (b.pos.y+(dt/10.0)*b.speed.y);
	}
	
	class DrawPanel extends JPanel {
		public DrawPanel() {
			setBackground(Color.WHITE);
		}
		
		@Override
		public Dimension getPreferredSize() {
			return new Dimension(SCREEN_X,SCREEN_Y);
		}
		
		@Override
		public Dimension getMinimumSize() {
			return getPreferredSize();
		}
		
		
	}
	
	public static void main(String[] args) {
		new AgarIOClient();
	}

	@Override
	public void keyPressed(KeyEvent e) {
		if(!keyPressed) {
			keyPressed = true;
			switch(e.getKeyCode()) {
			case KeyEvent.VK_SPACE: nI.split();
			break;
			case KeyEvent.VK_W: nI.shoot();
			break;
			}
		}
	}

	@Override
	public void keyReleased(KeyEvent e) {
		keyPressed = false;
	}

	@Override
	public void keyTyped(KeyEvent e) {
		
	}
}
