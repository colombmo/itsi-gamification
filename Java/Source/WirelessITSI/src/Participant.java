
public class Participant {
	private String firstName, lastName, color;
	private int score;
	private int position;
	
	/**
	 * Constructors
	 */

	public Participant(String firstName, String lastName, String color) {
		this.firstName = firstName;
		this.lastName = lastName;
		this.color = color;
		this.score = 1;
		this.position = 999;
	}
	
	public Participant(String firstName, String lastName, String color, int score) {
		this.firstName = firstName;
		this.lastName = lastName;
		this.color = color;
		this.score = score;
	}

	public String getFirstName() {
		return firstName;
	}

	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}

	public String getLastName() {
		return lastName;
	}

	public void setLastName(String lastName) {
		this.lastName = lastName;
	}

	public String getColor() {
		return color;
	}

	public void setColor(String color) {
		this.color = color;
	}

	public int getScore() {
		return score;
	}

	public void setScore(int score) {
		this.score = score;
	}
		
	public int getPosition() {
		return position;
	}

	public void setPosition(int position) {
		this.position = position;
	}
	
}
