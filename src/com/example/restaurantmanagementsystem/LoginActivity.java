package com.example.restaurantmanagementsystem;


import org.json.JSONException;
import org.json.JSONObject;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class LoginActivity extends Activity {
	Button btnSubmit = null;
	EditText txtUsername = null;
	EditText txtPassword = null;
	String jsonString = null;
	String urlParameters = "";
	String LOGIN_URL = "https://amit9oct.pythonanywhere.com/mobile_applications/verify_cred/";
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.login_activity);
		txtUsername = (EditText)findViewById(R.id.editTxtUsr);
		txtPassword =(EditText)findViewById(R.id.editTxtPass);
		btnSubmit = (Button)findViewById(R.id.login_button);
	}

	public void submit(View view){
		String username = txtUsername.getText().toString();
		String password = txtPassword.getText().toString();
		User user = null;
		if(username.length()>0 && password.length()>0){
			//Proceed further
		      urlParameters = "username="+username+"&"+"password="+password;
		      Log.i("submit()","url set "+urlParameters);
		      jsonString = null;
		      try {
		    	Log.i("submit()"," trying to submit url");
		    	jsonString = new FetchUserInfo(this, LOGIN_URL, urlParameters).execute().get();
		    	
		      } catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
		      }
		      Log.i("submit() ",jsonString);
		      JSONObject json = null;
		      if(jsonString!=null){
		    	  try {
						json = new JSONObject(jsonString);
						if(json.get("message").toString().equals("USER_PRESENT")){
				    		  Log.i("submit","user is present!!");
				    		  user = new User(json.get("username").toString(),json.get("name").toString());
				    		  Log.i("submit",user.toString());
				    	}
						else{
							Toast.makeText(getApplicationContext(), "Please register user not present.", 
						  		      Toast.LENGTH_SHORT).show();
						}
				  }catch (JSONException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
				  }
		    	  
		      }
		      if(user!=null){
		    	  Log.i("submit","User has been created!!");
		    	  Intent intent = new Intent(LoginActivity.this,RestIdDetails.class);
		    	  intent.putExtra("userObject", user);
		    	  startActivity(intent);
		      }
		}
		else{
		      Toast.makeText(getApplicationContext(), "Fill username and password!!", 
		      Toast.LENGTH_SHORT).show();
		}
	}
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.login, menu);
		return true;
	}

}
class FetchUserInfo extends AsyncTask<String, Void, String>{

	ProgressDialog dialog;
	Context context;
	String LOGIN_URL;
	String urlParameters;
	@Override
	protected String doInBackground(String... params) {
		// TODO Auto-generated method stub
		if(params.length>1){
			LOGIN_URL = (String) params[0];
			urlParameters  =(String) params[1];
		}
		try {
			Log.i("Async","Sending request!!!!!!!!");
			return SendRequest.sendPost(LOGIN_URL, urlParameters);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}  
	@Override
    protected void onPreExecute() {
		Toast.makeText(this.context, "Redirecting...", Toast.LENGTH_SHORT).show();
		dialog = ProgressDialog.show(this.context,"PLEASE WAIT","LOADING JOBS...", true);
		dialog.show();
		Log.i("Async","Runs!!!");
	} 
	@Override
	protected void onPostExecute(String res){
		dialog.dismiss();
	}
	
	public FetchUserInfo(Context context,String LOGIN_URL,String urlParameter){
		this.LOGIN_URL = LOGIN_URL;
		this.urlParameters = urlParameter;
		this.context = context;
		
	}
}
