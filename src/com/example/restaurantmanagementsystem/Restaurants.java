package com.example.restaurantmanagementsystem;

import java.io.Serializable;
import java.util.ArrayList;

public class Restaurants implements Serializable {
	private static final long serialVersionUID = -8100696520605456983L;
	private String name = null;
	public ArrayList<String> menuList = null;
	private int count = 0;
	private String location = null;
	public Restaurants(String name,String menu,int count) {
		// TODO Auto-generated constructor stub
		this.name = name.split(";")[0];
		this.location = name.split(";")[1];
		this.menuList = new ArrayList<String>();
		this.count = count;
		String[] menu_list = menu.split("',");
		for(int i=0;i<this.count;i++){
			menuList.add(menu_list[i].substring(1));
		}
	}
	public String getName() {
		return name;
	}
	public int getCount() {
		return count;
	}
	public String getLocation() {
		return location;
	}
	public void setName(String name) {
		this.name = name;
	}
	public void setCount(int count) {
		this.count = count;
	}
	public void setLocation(String location) {
		this.location = location;
	}
	@Override
	public String toString(){
		return this.name;
	}
}
