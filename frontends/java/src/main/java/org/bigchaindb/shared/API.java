package org.bigchaindb.shared;

import com.sun.jna.*;


public class API {
    interface Handoff extends Callback {
    	String getResult();
		void callback(String s);
	}
    
    interface SharedObject extends Library {
    	SharedObject INSTANCE = (SharedObject)
    			Native.loadLibrary("bigchaindb_shared", SharedObject.class);
    	void jsonRPC(String request, Callback fn);
    }
	
	public String jsonRPC(String request) {
		Handoff fn = new Handoff() {
			String result;
			public void callback(String json) { result = json; }
			public String getResult() { return result; }
		};
		SharedObject.INSTANCE.jsonRPC(request, fn);
		return fn.getResult();
	}
}