//
// Created by Feus on 2023/04/10.
//

#ifndef CLEANSW_TIMECARDTRANSACTION_H
#define CLEANSW_TIMECARDTRANSACTION_H


class TimeCardTransaction {
public:
	virtual ~TimeCardTransaction();
	TimeCardTransaction(long date, double hours, int empid);

	virtual void Execute();

private:
	int itsEmpid;
	long itsDate;
	double itsHours;
};


#endif //CLEANSW_TIMECARDTRANSACTION_H
