from datetime import datetime, date
import csv
from typing import List, Dict, Set, Optional
from pydantic import BaseModel, Field, ValidationError

class CSVRow(BaseModel):
    transaction_date: date = Field(validation_alias='Data transakcji')
    expense_amount: Optional[str] = Field(default=None, validation_alias='Obciążenia')
    income_amount: Optional[str] = Field(default=None, validation_alias='Uznania')
    transaction_description: str = Field(validation_alias='Opis')
    transaction_recipient: str = Field(validation_alias='Odbiorca/Zleceniodawca')

    model_config = {
        'populate_by_name': True,
        'arbitrary_types_allowed': True
    }

class ParsedTransaction(BaseModel):
    date: date
    type_id: int
    amount: float
    description: str

    model_config = {
        'arbitrary_types_allowed': True
    }

class BaseParser:
    required_columns: Set[str] = set()
    
    def validate_structure(self, file_content: str) -> List[str]:
        errors = []
        try:
            csv_lines = file_content.splitlines()
            if not csv_lines:
                return ["Plik jest pusty"]
            
            reader = csv.DictReader(csv_lines, delimiter=',')
            available_columns = set(reader.fieldnames) if reader.fieldnames else set()
            missing_columns = self.required_columns - available_columns
            
            if missing_columns:
                errors.append(
                    f"Brak wymaganych kolumn w pliku CSV: {', '.join(missing_columns)}"
                )
        except Exception as e:
            errors.append(f"Błąd podczas parsowania pliku CSV: {str(e)}")
            
        return errors

    def parse(self, file_content: str) -> List[ParsedTransaction]:
        raise NotImplementedError("Each parser must implement parse method")

class MilleniumCSVParser(BaseParser):
    required_columns = {'Data transakcji', 'Obciążenia', 'Uznania', 'Opis', 'Odbiorca/Zleceniodawca'}

    def _parse_amount(self, value: str) -> Optional[float]:
        """Convert string amount to float, handling empty strings and commas."""
        if not value or value.isspace():
            return None
        return float(value.replace(',', '.'))

    def parse(self, file_content: str) -> List[ParsedTransaction]:
        structure_errors = self.validate_structure(file_content)
        if structure_errors:
            raise ValueError(structure_errors[0])

        csv_lines = file_content.splitlines()
        csv_reader = csv.DictReader(csv_lines, delimiter=',')
        parsed_data = []
        validation_errors = []

        for row_idx, row in enumerate(csv_reader, start=1):
            try:
                # Validate row using Pydantic
                csv_row = CSVRow(**row)
                
                # Determine transaction type and amount
                type_id = None
                amount = 0

                expense = self._parse_amount(csv_row.expense_amount)
                income = self._parse_amount(csv_row.income_amount)

                if expense is not None:
                    type_id = 1  # Expense
                    amount = abs(expense)
                elif income is not None:
                    type_id = 2  # Income
                    amount = abs(income)
                else:
                    raise ValueError("Brak kwoty transakcji")

                # Create parsed transaction
                transaction = ParsedTransaction(
                    date=csv_row.transaction_date,
                    type_id=type_id,
                    amount=amount,
                    description=csv_row.transaction_description or csv_row.transaction_recipient
                )
                parsed_data.append(transaction)

            except ValidationError as e:
                validation_errors.append(f"Błąd w wierszu {row_idx}: {str(e)}")
            except ValueError as e:
                validation_errors.append(f"Błąd w wierszu {row_idx}: {str(e)}")

        if validation_errors:
            raise ValueError("\n".join(validation_errors))

        return parsed_data

def get_parser(bank_type: str) -> BaseParser:
    parsers = {
        'millenium': MilleniumCSVParser()
    }
    return parsers.get(bank_type.lower()) 