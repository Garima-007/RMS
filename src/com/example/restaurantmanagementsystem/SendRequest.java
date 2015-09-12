package com.example.restaurantmanagementsystem;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

import android.os.AsyncTask;
import android.util.Log;

public class SendRequest extends AsyncTask<String,Void,String> {
	private static final String USER_AGENT = "Mozilla/5.0";
 
	// HTTP GET request
	public static String sendGet(String url) throws Exception {
 
		//String url = "http://www.google.com/search?q=mkyong";
 
		URL obj = new URL(url);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();
 
		// optional default is GET
		con.setRequestMethod("GET");
 
		//add request header
		con.setRequestProperty("User-Agent", USER_AGENT);
 
		int responseCode = con.getResponseCode();
		//Log.i("SendRequest","\nSending 'GET' request to URL : " + url);
		//Log.i("SendRequest","Response Code : " + responseCode);
 
		BufferedReader in = new BufferedReader(
		        new InputStreamReader(con.getInputStream()));
		String inputLine;
		StringBuffer response = new StringBuffer();
 
		while ((inputLine = in.readLine()) != null) {
			response.append(inputLine);
		}
		in.close();
 
		//print result
		return response.toString();
 
	}
 
	// HTTP POST request
	public static String sendPost(String url,String urlParameters) throws Exception {
 
		//url = "https://amit9oct.pythonanywhere.com/mobile_applications/verify_cred/";
		URL obj = new URL(url);
		HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();
 
		//add reuqest header
		con.setRequestMethod("POST");
		con.setRequestProperty("User-Agent", USER_AGENT);
		con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");
		//String urlParameters = "username=amit9oct&password=1807";
		//String urlParameters = "restaurant_id=sharmas&user_id=smiley&algo=health_and_nutrition";
		//urlParameters = "username=amit9oct&password=1807";
		// Send post request
		con.setDoOutput(true);
		DataOutputStream wr = new DataOutputStream(con.getOutputStream());
		wr.writeBytes(urlParameters);
		wr.flush();
		wr.close();
 
		int responseCode = con.getResponseCode();
		//Log.i("SendRequest","\nSending 'POST' request to URL : " + url);
		//Log.i("SendRequest","Post parameters : " + urlParameters);
		//Log.i("SendRequest","Response Code : " + responseCode);
 
		BufferedReader in = new BufferedReader(
		        new InputStreamReader(con.getInputStream()));
		String inputLine;
		StringBuffer response = new StringBuffer();
 
		while ((inputLine = in.readLine()) != null) {
			response.append(inputLine);
		}
		in.close();
 
		//print result
		return response.toString();
 
	}

	@Override
	protected String doInBackground(String... params) {
		if(params[0].equals("POST")){
			try {
				sendPost(params[1], params[2]);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		if(params[0].equals("GET")){
			try {
				sendGet(params[1]);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		return null;
	}

}
