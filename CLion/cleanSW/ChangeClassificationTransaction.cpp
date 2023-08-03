//
// Created by Feus on 2023/04/10.
//

#include "ChangeClassificationTransaction.h"

ChangeClassificationTransaction::~ChangeClassificationTransaction() noexcept {}

ChangeClassificationTransaction::ChangeClassificationTransaction(int empid)
	: ChangeEmployeeTransaction(empid){

}

void ChangeClassificationTransaction::Change(Employee &) {
	e.SetClassification(GetClassification());
	e.SetSchedule(GetSchedule());
}