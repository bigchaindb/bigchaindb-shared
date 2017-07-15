import static org.junit.Assert.*;

import org.bigchaindb.shared.API;
import org.junit.Test;


public class TestMain {
	API api = new API();
	
	@Test
	public void test() {
		String request = "{\"method\": \"generateKeyPair\",\"params\":{}}";
		String res = api.jsonRPC(request);
		assertTrue(res.contains("public_key"));
	}
}