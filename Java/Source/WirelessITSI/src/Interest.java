
public class Interest {
	private String description;
	private String color;
	private int score;
	
	public Interest(String description, String color) {
		this.description = description;
		this.color = color;
		this.score = 0;
	}
	
	public Interest(String description, String color, int score) {
		this.description = description;
		this.color = color;
		this.score = score;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public String getColor() {
		return color;
	}

	public void setColor(String color) {
		this.color = color;
	}

	@Override
	public String toString() {
		return "Interest [description=" + description + ", color=" + color
				+ "]";
	}

	public int getScore() {
		return score;
	}

	public void setScore(int score) {
		this.score = score;
	}	
}
