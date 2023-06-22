"""
Module Name: transaction_manager
Author: Equipe 3
Purpose: Gerenciador de bloqueios em itens de dados.
Created: 2023-06-19
"""
import re

from settings import debug_message, init_logger, inspect_type
from lock_manager import LockManager

from typing import Dict, List

logger = init_logger(__name__)

class Query:
    def __init__(self, query_string: str, parent_transaction: str, reference_lock_manager: LockManager) -> None:
        debug_message(
            f"""Query: __init__:
                query_string = {query_string}
                parent_transaction = {parent_transaction}
                inspect_type(reference_lock_manager) = {inspect_type(reference_lock_manager)}
                reference_lock_manager = {reference_lock_manager}
            """
        )
        if query_string.startswith("READ(") and query_string.endswith(")"):
            self.operation = "READ"
            self.variable = query_string[5:-1]
        elif query_string.startswith("WRITE(") and query_string.endswith(")"):
            self.operation = "WRITE"
            self.variable = query_string[6:-1]
        else:
            self.operation = "NO-OP"
            self.variable = None
        self.query_string = query_string
        self.status = "READY"
        self.transaction = parent_transaction
        self.lock_manager = reference_lock_manager
    
    def get_query_string(self) -> str:
        return self.query_string    

    def get_operation(self) -> str:
        return self.operation

    def get_variable(self) -> str:
        return self.variable

    def get_status(self) -> str:
        debug_message(
            f"""Query: get_status (exit):
                inspect_type(self.status) = {inspect_type(self.status)}
                self.status = {self.status}
            """
        )
        return self.status

    def get_lock(self) -> str:
        debug_message(
            f"""Query: get_lock:
             inspect_type(self.transaction) = {inspect_type(self.transaction)}
                self.transaction = {self.transaction}
                inspect_type(self.operation) = {inspect_type(self.operation)}
                self.operation = {self.operation}
                inspect_type(self.variable) = {inspect_type(self.variable)}
                self.variable = {self.variable}
            """
        )
        if self.operation == "READ":
            self.status = self.lock_manager.acquire_shared_lock(self.variable, self.transaction)["result"]
        elif self.operation == "WRITE":
            self.status = self.lock_manager.acquire_exclusive_lock(self.variable, self.transaction)["result"]
        elif self.operation == "NO-OP":
            self.status = "SUCCESS"
        else:
            self.status = "UNKNOWN STATE"
        debug_message(
            f"""Query: get_lock (exit):
                inspect_type(self.status) = {inspect_type(self.status)}
            """
        )
        return self.status

    def release_lock(self) -> str:
        self.status = "SUCCESS"
        return self.lock_manager.release_lock(self.variable, self.transaction)


class Transaction:
    def __init__(self, queries: str, reference_lock_manager: LockManager) -> None:
        debug_message(
            f"""Transaction: __init__:
                inspect_type(queries) = {inspect_type(queries)}
                queries = {queries}
            """
        )
        self.transaction_string = queries
        queries = queries.strip().strip('[]').replace("\r\n", "\n")
        query_strings = [item.strip() for item in re.split(r',|;|\n', queries) if item and not item.startswith(("--", "# "))]
        self.queries = [Query(query_string, queries, reference_lock_manager) for query_string in query_strings]
        self.lock_manager = reference_lock_manager
        self.phase = "Expanding"
        self.status = "READY"

    def get_transaction_string(self):
        return self.transaction_string
    
    def get_status(self):
        return self.status

    def has_waiting_query(self) -> bool:
        for query in self.queries:
            if query.get_status() == "WAIT":
                return True
        return False

    def step_into(self) -> str:
        debug_message("Transaction: step_into")
        debug_message(
            f"""Transaction: step_into:
                inspect_type(self.transaction_string) = {inspect_type(self.transaction_string)}
                self.transaction_string = {self.transaction_string}
                inspect_type(self.status) = {inspect_type(self.status)}
                self.status = {self.status}
                inspect_type(self.phase) = {inspect_type(self.phase)}
                self.phase = {self.phase}
            """
        )
        situation = "INVALID STATUS"
        if self.status not in ["COMMITED", "KILLED"]:
            if self.status == "READY":
                self.status = "EXECUTING"

            if self.phase == "Expanding":
                pending_queries = [query for query in self.queries if query.get_status() in ["READY", "WAIT"]]
                if len(pending_queries) == 0:
                    self.phase = "Shrinking"
                else:
                    for query in pending_queries:
                        query.get_lock()
                    situation = "EXECUTING"

            elif self.phase == "Shrinking":
                active_queries = [query for query in self.queries if query.get_status() in ["READ", "WRITE"]]
                if len(active_queries) == 0:
                    self.status = "COMMITED"
                    situation = self.status
                else:
                    for query in active_queries:
                        query.release_lock()
        
            if self.has_waiting_query():
                situation = "WAITING"
        else:
            situation = self.status
        debug_message(
            f"""Transaction: step_into (exit):
                inspect_type(self.status) = {inspect_type(self.status)}
                inspect_type(self.phase) = {inspect_type(self.phase)}
                inspect_type(situation) = {inspect_type(situation)}
            """
        )
        return situation
        
    def die(self) -> str:
        self.status = "KILLED"
        for query in self.queries:
            query.release_lock()
        return self.status

class TransactionManager:
    def __init__(self, reference_lock_manager: LockManager, transactionList: List[str] = None) -> None:
        debug_message(
            f"""TransactionManager: __init__:
                inspect_type(reference_lock_manager) = {inspect_type(reference_lock_manager)}
                reference_lock_manager = {reference_lock_manager}
                inspect_type(transactionList) = {inspect_type(transactionList)}
                transactionList = {transactionList}
            """
        )
        if transactionList is None:
            # transactionList = [
            #     "[READ(Users);READ(Products);WRITE(Orders);]"
            #     ,"[READ(Users);WRITE(Users);WRITE(Orders);]"
            #     ,"[WRITE(Orders);READ(Orders)]"
            # ]
            transactionList = [
                "READ(Users)"
                ,"WRITE(Users)"
                ,"READ(Orders)"
            ]

        self.lock_manager = reference_lock_manager
        self.transactionList: List[Transaction] = [Transaction(transaction_string, reference_lock_manager) for transaction_string in transactionList]

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactionList.append(transaction)

    def remove_transaction(self, transaction: Transaction) -> None:
        self.transactionList.remove(transaction)

    def list_transactions(self) -> List[Transaction]:
        return [transaction.get_transaction_string() for transaction in self.transactionList]

    def list_locks(self) -> List[Dict[str, str]]:
        debug_message("TransactionManager: list_locks")
        data_items: List[str] = self.lock_manager.list_data_items()
        transactions: List[str] = ["Transação<br>" + transaction.get_transaction_string() for transaction in self.transactionList]
        locksTable: List[Dict[str, str]] = []
        for data_item in data_items:
            rowDict: Dict[str, str] = {}
            rowDict["Item de Dados"] = data_item
            for transaction in transactions:
                rowDict[transaction] = self.lock_manager.get_lock_status(data_item, transaction)
            locksTable.append(rowDict)
        debug_message(
            f"""TransactionManager: list_locks:
                inspect_type(locksTable) = {inspect_type(locksTable)},
                locksTable = {locksTable}"""
        )
        return locksTable

    def step_into(self) -> List[Dict[str, str]]:
        debug_message("TransactionManager: step_into")
        [transaction.step_into() for transaction in self.transactionList]
        return self.list_locks()