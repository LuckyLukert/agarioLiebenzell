package de.liebenzellAgarIo.kai;

import java.io.*;
import java.net.*;
import java.util.*;

import javax.swing.JOptionPane;

import org.json.simple.parser.*;
import org.json.simple.*;

public class NetworkCommunication implements Runnable{
	private Socket socket;
	public static final int PORT = 60001;
	
	private BufferedReader in;
	private BufferedWriter out;
	private NetworkInterface nI;
	
	private Thread reciver;
	private EventFirer eF;
	
	private Queue<String> toDo;
	
	public static final String EVENT = "event";
	public static final String WORLD = "world";
	public static final String ID = "id";
	public static final String PLAYER = "player";
	public static final String PLAYERS = "players";
	public static final String MOVES = "moves";
	public static final String BALLS = "balls";
	public static final String BALL = "ball";
	public static final String NAME = "name";
	public static final String DIRECTION = "direction";
	public static final String FOOD = "food";
	public static final String OBSTACLES = "obstacles";
	public static final String POS = "position";
	public static final String SPEED = "speed";
	public static final String SIZE = "size";
	public static final String COLOR = "color";
	public static final String X = "x";
	public static final String Y = "y";
	public static final String WIDTH = "width";
	public static final String HEIGHT = "height";

	
	//Server to Client
	public static final String JOIN = "join";
	public static final String JOIN_WATCHER = "joinWatcher";
	public static final String PLAYER_JOINED = "playerJoined";
	public static final String PLAYER_KILLED = "playerKilled";
	public static final String PLAYER_MOVES = "playerMoves";
	public static final String OBSTACLE_ADD = "obstacleAdd";
	public static final String OBSTACLE_REMOVE = "obstacleRemove";
	public static final String FOOD_ADD = "foodAdd";
	public static final String FOOD_REMOVE = "foodRemove";
	public static final String FOOD_MOVE = "foodMove";
	
	//client to Server
	public static final String WANT_TO_JOIN = "wantToJoin";
	public static final String WANT_TO_WATCH = "wantToWatch";
	public static final String MOVE = "move";
	public static final String SHOOT = "shoot";
	public static final String SPLIT = "split";

	
	public NetworkCommunication(String name,String ip,NetworkInterface nI) {
		this.nI = nI;
		
//		int port = Integer.parseInt(JOptionPane.showInputDialog("Port"));
		
		try {
			InetAddress addr = InetAddress.getByName(ip);
		
			socket = new Socket(addr, PORT);
			
			in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
			
		} catch(Exception e) {
			System.err.println(e.getMessage());
		}
		
		
		toDo = new LinkedList<>();
		
		reciver = new Thread(this);
		reciver.start();
		eF = new EventFirer();
		
		eF.start();
		
		join(name);
		
	}
	
	private void join(String name) {
		JSONObject join = new JSONObject();
		join.put(EVENT, WANT_TO_JOIN);
		
		
		join.put(NAME, name);
		
		send(join);
		
	}

	private void send(JSONObject data) {
		try {
			out.write(data.toJSONString()+"\n");
			out.flush();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
//		System.out.println(data.toJSONString());
	}
	
	public void move(Vector direction) {
		JSONObject data = new JSONObject();
		data.put(EVENT, MOVE);
		
		JSONObject vector = new JSONObject();
		vector.put(X,direction.x);
		vector.put(Y,direction.y);
		
		data.put(DIRECTION, vector);
		
		send(data);
	}
	
	public void shoot() {
		JSONObject data = new JSONObject();
		data.put(EVENT, SHOOT);
		send(data);
		
	}
	
	public void split() {
		JSONObject data = new JSONObject();
		data.put(EVENT, SPLIT);
		send(data);
	}
	
	public static void main(String[] args) {
		NetworkCommunication nC = new NetworkCommunication("blub", "127.0.0.1",null);
		nC.move(new Vector(12, 34));
	}

	@Override
	public void run() {
		System.out.println("Recieving messages");
		
		while(true) {
			try {
				String line = in.readLine();
//				System.out.println("msg: " + line);
				synchronized(toDo) {
					toDo.offer(line);
					toDo.notify();
				}
			} catch (IOException e) {
			}
		}
	}
	
	class EventFirer extends Thread{
		public void run() {
			JSONParser p = new JSONParser();
			while(true) {
				String line = null;
				synchronized (toDo) {
					while(toDo.isEmpty()) {try {
						toDo.wait();
					} catch (InterruptedException e) {
						e.printStackTrace();
					}}
					line = toDo.poll();
				}
				
				try {
					JSONObject o = (JSONObject) p.parse(line);
					
					String event = (String) o.get(EVENT);
					
					switch(event) {
					case JOIN: nI.join(getWorld((JSONObject) o.get(WORLD)), Integer.parseInt(o.get(ID).toString()));
						break;
					case JOIN_WATCHER: nI.joinWatcher(getWorld((JSONObject) o.get(WORLD)));
						break;
					case PLAYER_JOINED: nI.playerJoined(Integer.parseInt(o.get(ID).toString()), getPlayer((JSONObject) o));
						break;
					case PLAYER_KILLED: nI.playerKilled(Integer.parseInt(o.get(ID).toString()));
						break;
					case PLAYER_MOVES:JSONArray arr = (JSONArray) o.get(MOVES);
						for(Object obj: arr) {
							JSONObject jO = (JSONObject) obj;
							LinkedList<Ball> l = new LinkedList<>();
							JSONArray balls = (JSONArray) jO.get(BALLS);
							for(Object b:balls) {
								l.add(getBall((JSONObject) b));
							}
							nI.playerMoves(Integer.parseInt(jO.get(ID).toString()),l);
						}
						break;
					case OBSTACLE_ADD: nI.obstacleAdd(Integer.parseInt(o.get(ID).toString()), getBall((JSONObject) o.get(BALL)));
						break;
					case OBSTACLE_REMOVE: nI.obstacleRemove(Integer.parseInt(o.get(ID).toString()));
						break;
					case FOOD_ADD: nI.foodAdd(Integer.parseInt(o.get(ID).toString()), getBall((JSONObject) o.get(BALL)));
						break;
					case FOOD_REMOVE: nI.foodRemove(Integer.parseInt(o.get(ID).toString()));
						break;
					case FOOD_MOVE: nI.foodMove(Integer.parseInt(o.get(ID).toString()), getBall((JSONObject) o.get(BALL)));
						break;
					}
					
				} catch (ParseException e) {
					System.out.println("error parsing at: " + e.getPosition());
				}
				
				
				
			}
		}
		
		public Point getPoint(JSONObject o) {
//			System.out.println("Point: " + o);
			return new Point((Double.valueOf(o.get(X).toString())), Double.valueOf(o.get(Y).toString()));
		}
		
		public Vector getVector(JSONObject o) {
//			System.out.println("Vector: " + o);
			return new Vector(Double.valueOf(o.get(X).toString()), Double.valueOf( o.get(Y).toString()));
		}
		
		public Ball getBall(JSONObject o) {
			Vector speed = getVector((JSONObject) o.get(SPEED));
			Point pos = getPoint((JSONObject) o.get(POS));
			return new Ball(pos,speed,Double.parseDouble(o.get(SIZE).toString()),(String) o.get(COLOR));
		}
		
		public Player getPlayer(JSONObject o) {
			System.out.println(o);
			JSONArray arr = (JSONArray) o.get(BALLS);
			LinkedList<Ball> balls = new LinkedList<>();
			for(Object obj:arr) {
				balls.add(getBall((JSONObject) obj));
			}
			
			return new Player((String) o.get(NAME),balls);
			
		}
		
		public World getWorld(JSONObject o) {
			System.out.println(o.toJSONString());
			
			JSONObject f = (JSONObject) o.get(FOOD);
			HashMap<Integer,Ball> food = new HashMap<>();
			for(Object obj:f.keySet()) {
				food.put((Integer.parseInt((String) obj)), getBall((JSONObject) f.get(obj)));
			}
			
			JSONObject p = (JSONObject) o.get(PLAYERS);
			HashMap<Integer, Player> players = new HashMap<>();
			for(Object obj:p.keySet()) {
//				System.out.println(obj);
				players.put((Integer.parseInt((String) obj)), getPlayer((JSONObject) p.get(obj)));
			}
			
			JSONObject ob = (JSONObject) o.get(OBSTACLES);
			HashMap<Integer,Ball> obstacles = new HashMap<>();
			for(Object obj:ob.keySet()) {
				obstacles.put((Integer.parseInt((String) obj)), getBall((JSONObject) ob.get(obj)));
			}
			
			
			return new World(food, obstacles, players,Integer.parseInt(o.get(WIDTH).toString()),Integer.parseInt(o.get(HEIGHT).toString()));
		}
		
	
	}
}
