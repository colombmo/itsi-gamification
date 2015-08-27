
public class UpdateScore implements Runnable{
	IndividualView indiv;
	
	public UpdateScore(IndividualView indiv){
		this.indiv = indiv;
	}
	
	@Override
	public void run() {
		while(IndividualView.flag){
			indiv.updateScores();
		}
	}

}
