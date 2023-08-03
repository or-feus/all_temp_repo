//
// Created by Feus on 2023/04/10.
//

#include "TimeCardTransaction.h"
#include "PayrollDatabase.h"
#include "TimeCard.h"

extern PayrollDatabase GpayrollDatabase;

TimeCardTransaction::~TimeCardTransaction() {

}

TimeCardTransaction::TimeCardTransaction(long date, double hours, int empid)
		: itsDate(date), itsHours(hours), itsEmpid(empid) {
}

void TimeCardTransaction::Execute() {
	Employee *e = GpayrollDatabase.GetEmployee(itsEmpid);
	if (e) {
		PaymentClassification *pc = e->GetClassification();
		if(HourlyClassification* hc = dynamic_cast<HourlyClassification*>(pc)){
			hc->AddTimeCard(new TimeCard(itsDate, itsHours));
		}else{
			throw ("Tried to add timecard to non-hourly employee");
		}
	}else{
		throw ("No such employee");
	}
}