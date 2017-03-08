package de.liebenzellAgarIo.kai;

public class Ball {
	Point pos;
	Vector speed;
	String color;
	double size;

	public Ball(Point pos, Vector speed, double size,String color) {
		this.pos = pos;
		this.speed = speed;
		this.size = Math.sqrt(size);
		this.color = color;
	}
	
	
}
