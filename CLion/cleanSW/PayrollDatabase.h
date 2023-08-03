//
// Created by Feus on 2023/04/08.
//

#ifndef CLEANSW_PAYROLLDATABASE_H
#define CLEANSW_PAYROLLDATABASE_H
#include <map>

using namespace std;

class Employee;

class PayrollDatabase {
public:
	virtual ~PayrollDatabase();

	Employee *GetEmployee(int empId);
	void AddEmployee(int empId, Employee *);
	void clear(){
		itsEmployees.clear();
	}
private:

	map<int, Employee*> itsEmployees;
};





#endif //CLEANSW_PAYROLLDATABASE_H
