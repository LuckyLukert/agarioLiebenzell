package de.liebenzellAgarIo.kai;

import java.util.*;

public interface NetworkInterface {
	public void join(World world,int id);
	public void joinWatcher(World world);
	public void playerJoined(int id,Player player);
	public void playerKilled(int id);
	public void playerMoves(int id,LinkedList<Ball> balls);
	public void obstacleAdd(int id,Ball ball);
	public void obstacleRemove(int id);
	public void foodAdd(int id,Ball ball);
	public void foodRemove(int id);
	public void foodMove(int id,Ball ball);
	
}
