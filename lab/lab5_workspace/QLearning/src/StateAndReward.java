public class StateAndReward {

	
	/* State discretization function for the angle controller */
	public static String getStateAngle(double angle, double vx, double vy) {

		/* TODO: IMPLEMENT THIS FUNCTION */
		
		String state = Integer.toString(discretize(angle, 8, -Math.PI/4, Math.PI/4));
		
		return state;
	}

	/* Reward function for the angle controller */
	public static double getRewardAngle(double angle, double vx, double vy) {

		/* TODO: IMPLEMENT THIS FUNCTION */
		
		double reward = 0;
		int stateReward = discretize(angle, 8, -Math.PI/4, Math.PI/4);
		if( stateReward < 2 ) {
			reward = 0.25;
		} 
		else if(stateReward > 2 && stateReward < 4) {
			reward = 0.5;
		}
		else if(stateReward == 4 ) {
			reward = 1;
		}
		else if(stateReward > 4 && stateReward < 6) {
			reward = 0.5;
		}
		else {
			reward = 0.25;
		}

		return reward;
	}

	/* State discretization function for the full hover controller */
	public static String getStateHover(double angle, double vx, double vy) {

		/* TODO: IMPLEMENT THIS FUNCTION */
		String state;
		int a = discretize2(angle, 10, -Math.PI/4, Math.PI/4);
		
		if(a == 0)
			state = "a0";
		else if(a==1)
			state = "a1";
		else if(a==2)
			state = "a2";
		else if(a==3)
			state = "a3";
		else if(a==4)
			state = "a4";
		else if(a==5)
			state = "a5";
		else if(a==6)
			state = "a6";
		else if(a==7)
			state=  "a7";
		else if(a==8)
			state=  "a8";
		else 
			state = "a9";
		
		int b = discretize2(vx, 2, -1, 1);
		
		if(b == 0)
			state=state+ "x0";
		else if(b==1)
			state=state+ "x1";
		else if(b==2)
			state=state+ "x2";
		else 
			state=state+ "x3";
		
		int c = discretize2(vy, 10, -1, 1);
		if(c == 0)
			state=state+ "y4";
		else if(c==1)
			state=state+ "y5";
		else if(c==2)
			state=state+ "y6";
		else if(c==3)
			state=state+ "y7";
		else if(c==4)
			state=state+ "y8";
		else if(c==5)
			state=state+ "y9";
		else if(c==6)
			state=state+ "y10";
		else if(c==5)
			state=state+ "y11";
		else if(c==6)
			state=state+ "y12";
		else 
			state=state+ "y13";
		
		return state;
	}

	/* Reward function for the full hover controller */
	public static double getRewardHover(double angle, double vx, double vy) {

		/* TODO: IMPLEMENT THIS FUNCTION */

		String s = StateAndReward.getStateHover(angle, vx, vy);
		double reward = 0;
		
		if(s.contains("a5") && (s.contains("x2") || s.contains("x1") || s.contains("x3")) && (s.contains("y9") || s.contains("y8") || s.contains("y10"))) {
			reward = 1;
		} else {
			if(s.contains("a4") && s.contains("x1") && s.contains("y8")) {
				reward = 0.8;
			}
			else {
				if(s.contains("a6") && s.contains("x3") && s.contains("y10")) {
					reward = 0.8;
				}
				else {
					reward = -1;
				}
			}
		}
		
		
		return reward;
	}

	// ///////////////////////////////////////////////////////////
	// discretize() performs a uniform discretization of the
	// value parameter.
	// It returns an integer between 0 and nrValues-1.
	// The min and max parameters are used to specify the interval
	// for the discretization.
	// If the value is lower than min, 0 is returned
	// If the value is higher than min, nrValues-1 is returned
	// otherwise a value between 1 and nrValues-2 is returned.
	//
	// Use discretize2() if you want a discretization method that does
	// not handle values lower than min and higher than max.
	// ///////////////////////////////////////////////////////////
	public static int discretize(double value, int nrValues, double min,
			double max) {
		if (nrValues < 2) {
			return 0;
		}

		double diff = max - min;

		if (value < min) {
			return 0;
		}
		if (value > max) {
			return nrValues - 1;
		}

		double tempValue = value - min;
		double ratio = tempValue / diff;

		return (int) (ratio * (nrValues - 2)) + 1;
	}

	// ///////////////////////////////////////////////////////////
	// discretize2() performs a uniform discretization of the
	// value parameter.
	// It returns an integer between 0 and nrValues-1.
	// The min and max parameters are used to specify the interval
	// for the discretization.
	// If the value is lower than min, 0 is returned
	// If the value is higher than min, nrValues-1 is returned
	// otherwise a value between 0 and nrValues-1 is returned.
	// ///////////////////////////////////////////////////////////
	public static int discretize2(double value, int nrValues, double min,
			double max) {
		double diff = max - min;

		if (value < min) {
			return 0;
		}
		if (value > max) {
			return nrValues - 1;
		}

		double tempValue = value - min;
		double ratio = tempValue / diff;

		return (int) (ratio * nrValues);
	}

}
