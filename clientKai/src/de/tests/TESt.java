package de.tests;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class TESt {
	public static void main(String args[]) {
		ServerSocket server;
		BufferedReader in = null;
		BufferedWriter out = null;
		
		Scanner s = new Scanner(System.in);
		
		try {
			server = new ServerSocket(60001);
			Socket sock = server.accept();

			//Input/Output Streams anlegen
			in = new BufferedReader(new InputStreamReader(sock.getInputStream()));
			out = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
			
//			out.write("Hallo Welt\n");
//			out.flush();
//			System.out.println("Hello World");

		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		while(true) {
			try {
				System.out.println(in.readLine());
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
			try {
				out.write(s.nextLine()+"\n");
				out.flush();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
		}
	}
}
