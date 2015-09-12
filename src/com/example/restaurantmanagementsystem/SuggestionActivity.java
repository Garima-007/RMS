package com.example.restaurantmanagementsystem;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

public class SuggestionActivity extends Activity {
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		Log.i("reached","suggestion");
		setContentView(R.layout.suggestion_activity);
	}
}
