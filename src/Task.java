package logic;

import java.util.ArrayList;

public class Task {
    private String name;
    private int duration;
    private ArrayList<String> dependencies;
    private int ES, EF, LS, LF, slack;

    public Task(String name, int duration, ArrayList<String> dependencies) {
        this.name = name;
        this.duration = duration;
        this.dependencies = dependencies;
        this.ES = this.EF = this.LS = this.LF = this.slack = 0;
    }

    public String getName() { return name; }
    public int getDuration() { return duration; }
    public ArrayList<String> getDependencies() { return dependencies; }
    public int getES() { return ES; }
    public void setES(int ES) { this.ES = ES; }
    public int getEF() { return EF; }
    public void setEF(int EF) { this.EF = EF; }
    public int getLS() { return LS; }
    public void setLS(int LS) { this.LS = LS; }
    public int getLF() { return LF; }
    public void setLF(int LF) { this.LF = LF; }
    public int getSlack() { return slack; }
    public void setSlack(int slack) { this.slack = slack; }
}
