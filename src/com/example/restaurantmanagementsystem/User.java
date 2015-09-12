package com.example.restaurantmanagementsystem;

import java.io.Serializable;

public class User implements Serializable {
	private static final long serialVersionUID = 5905319086099826848L;
	private String username = null;
	private String name = null;
	public String getUsername(){
		return this.username;
	}
	public String getName(){
		return this.name;
	}
	public User(String username,String name){
		this.username = username;
		this.name = name;
	}
	@Override
	public String toString(){
		return this.name;
	}
}
