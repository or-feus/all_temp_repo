//
// Created by Feus on 2023/04/08.
//

#ifndef CLEANSW_TRANSACTION_H
#define CLEANSW_TRANSACTION_H

class Transaction {
public:
	virtual ~Transaction();
	virtual void Execute() = 0;
};


#endif //CLEANSW_TRANSACTION_H
