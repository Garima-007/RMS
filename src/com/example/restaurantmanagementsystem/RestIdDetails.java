package com.example.restaurantmanagementsystem;

import org.json.JSONObject;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;


public class RestIdDetails extends Activity {
	TextView txtName = null;
	Button btnSearch = null;
	EditText txtSearch = null;
	TextView txtRestName = null;
	String LOAD_MENU_URL = "https://amit9oct.pythonanywhere.com/mobile_applications/load_menu/";
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.rest_id_activity);
		Toast.makeText(getApplicationContext(), "Redirecting...", Toast.LENGTH_SHORT).show();
		Intent intent = getIntent();
		User user = (User) intent.getSerializableExtra("userObject");
		txtName = (TextView)findViewById(R.id.txtName);
		txtName.setText("Wecome "+user+" !!!");
		txtSearch = (EditText) findViewById(R.id.txtRestSearch);
		btnSearch = (Button) findViewById(R.id.btnSearch);
		txtRestName = (TextView) findViewById(R.id.txtRestName);
		txtRestName.setText("");
	}
	public void load_menu(View view){
		String rest_id = txtSearch.getText().toString();
		Log.i("RestIdDeatials",rest_id);
		//Send request to server
		String menuString=null;
			try {
				StrictMode.enableDefaults();
				Toast.makeText(getApplicationContext(), "Loading Menu...", Toast.LENGTH_SHORT).show();
				String parameter = "restaurant_id="+rest_id;
				Log.i("RestIdDetails",parameter);
				menuString = SendRequest.sendPost(LOAD_MENU_URL,parameter);
				Toast.makeText(getApplicationContext(), "Loading Menu...",Toast.LENGTH_SHORT).show();
				Log.i("RestIdDetials",menuString);
				if(menuString!=null){
					JSONObject jsonMenu = new JSONObject(menuString);
					int count = jsonMenu.getInt("count");
					String name = jsonMenu.getString("name");
					String menu = jsonMenu.getString("menu");
					String[] sp = name.split(";");
					txtRestName.setText("\t\t"+sp[0]+"\n Location- "+sp[1]);
					menu = menu.substring(1, menu.length()-1);
					Log.i("RestIdDetials",menu);
					Restaurants rest = new Restaurants(name, menu, count);
					Log.i("RestIdDetails",rest.toString());
					Intent intent = new Intent(RestIdDetails.this,LoadMenuActivity.class);
					intent.putExtra("restaurantObject",rest);
					startActivity(intent);
				}else{
					Toast.makeText(getApplicationContext(), "Check internet connection!!",Toast.LENGTH_SHORT).show();
				}
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	}
}
