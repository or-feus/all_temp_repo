//
// Created by Feus on 2023/04/10.
//

#include "ChangeHourlyTransaction.h"

ChangeHourlyTransaction::~ChangeHourlyTransaction() noexcept {}

ChangeHourlyTransaction::ChangeHourlyTransaction(int empid, double hourlyRate)
	: ChangeClassificationTransaction(empid), itsHourlyRate(hourlyRate){

}

PaymentSchedule* ChangeHourlyTransaction::GetSchedule() const {
	return new WeeklySchedule();
}

PaymentClassification* ChangeHourlyTransaction::GetClassification() const {
	return new HourlyClassification(itsHourlyRate)
}