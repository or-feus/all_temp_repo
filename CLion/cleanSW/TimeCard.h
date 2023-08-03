//
// Created by Feus on 2023/04/10.
//

#ifndef CLEANSW_TIMECARD_H
#define CLEANSW_TIMECARD_H


class TimeCard {
public:
	virtual ~TimeCard();
	TimeCard(long date, double hours);
	long GetDate(){
		return itsDate;
	}
	double GetHour(){
		return itsHours;
	}
private:
	long itsDate;
	double itsHours;
};

#endif //CLEANSW_TIMECARD_H
