package de.liebenzellAgarIo.kai;

import java.util.HashMap;

public class World {
	HashMap<Integer,Ball> food;
	HashMap<Integer,Ball> obstacles;
	HashMap<Integer,Player> players;
	int width;
	int height;
	public World(HashMap<Integer, Ball> food, HashMap<Integer, Ball> obstacles, HashMap<Integer, Player> players,
			int width, int height) {
		this.food = food;
		this.obstacles = obstacles;
		this.players = players;
		this.width = width;
		this.height = height;
	}
	
	
	
}
