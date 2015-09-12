package com.example.restaurantmanagementsystem;


import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Toast;
import android.widget.LinearLayout.LayoutParams;
import android.widget.TextView;

public class LoadMenuActivity extends Activity {
	TextView txtRestName = null;
	OnClickListener suggestion_cat = new OnClickListener(){
		@Override
		public void onClick(View v){
			Log.i("hereeeeeeeeee","hjhhijijjjjjjjjjjjjjjjjjjjjjjjjjjjj");
			Toast.makeText(getApplicationContext(), "Under Construction...", Toast.LENGTH_SHORT).show();
		}
	};
	OnClickListener add_to_cart =new OnClickListener() {

		@Override
		public void onClick(View v) {
			// TODO Auto-generated method stub
			
		}
	};
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.menu_activity);
		Intent intent = getIntent();
		Log.i("LoadMenuActivity","!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
		Restaurants rest = (Restaurants) intent.getSerializableExtra("restaurantObject");
		LinearLayout mainLayout = (LinearLayout)findViewById(R.id.menu);
		mainLayout.setOrientation(LinearLayout.VERTICAL);
		//txtRestName = (TextView)findViewById(R.id.menu_top);
		//txtRestName.setText(rest.getName()+"'s Menu");
		String menuString="";
		int count = rest.getCount();
		for(int i=0;i<count;i++){
            // Create TextView
            String item = null;
            String temp = rest.menuList.get(i).substring(1);
            if (i==0)
            	item = rest.menuList.get(0);
            if(i>0 && i!=count-1)
            	item = (String) rest.menuList.get(i).substring(1);
            if(i==count-1)
            	item = temp.substring(0,temp.length()-1);
            Log.i("LoadMenuActivity","!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"+item);
            LinearLayout LL = new LinearLayout(this);
	    	LL.setOrientation(LinearLayout.HORIZONTAL);
	    	LayoutParams LLParams = new LayoutParams(LayoutParams.MATCH_PARENT,LayoutParams.MATCH_PARENT);
	    	LLParams.weight=1;
	    	LL.setLayoutParams(LLParams);
			for(int j=0;j<3;j++){
				Button cellButton = new Button(this);
            	cellButton.setHeight(50);
            	//cellButton.setWidth((int)(300*(3-j)/3.0));
            	cellButton.setId(i*3+j);
            	cellButton.setBackgroundResource(R.drawable.submit_bg);
            	if(j==0)
            		cellButton.setText(item);
            	else if(j==1)
            		cellButton.setText("Price");
            	else
            		cellButton.setText("Add");
            	if(j==2)
            		cellButton.setOnClickListener(add_to_cart);
            		LL.addView(cellButton,LLParams);
			}
			mainLayout.addView(LL);

            menuString += item;
            menuString += "\n";
		}
		Button suggestionButton =  new Button(this);
		suggestionButton.setHeight(50);
		suggestionButton.setText("Suggestions");
		suggestionButton.setOnClickListener(suggestion_cat);
		mainLayout.addView(suggestionButton);
	}
}
