
public class Table {
	private int id;
	private String descr;
	private int x;
	private int y;
	
	public Table(int id, String descr, int x, int y){
			this.id = id;
			this.descr = descr;
			this.x = x;
			this.y = y;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public int getX() {
		return x;
	}

	public void setX(int x) {
		this.x = x;
	}

	public int getY() {
		return y;
	}

	public void setY(int y) {
		this.y = y;
	}

	@Override
	public String toString() {
		return "Table [id=" + id + ", x=" + x + ", y=" + y + "]";
	}

	public String getDescr() {
		return descr;
	}

	public void setDescr(String descr) {
		this.descr = descr;
	}
}
