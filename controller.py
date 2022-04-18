class Controller:

    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._connect_signals()

    def calculate_button_actions(self):
        formula = self._view.get_formula_name()
        optional_info = self._view.get_aditional_info()
        charge = int(self._view.get_selected_charge())
        adduct = self._view.get_selected_adduct()
        logger_text_to_show = self._model.run_calculator(formula, charge, adduct)
        if optional_info != "":
            self._view.print_logger(optional_info)
        if logger_text_to_show == "Not found":
            self._view.not_found_element_pop_up()
            return
        if formula != "":
            self._view.print_logger(logger_text_to_show + "\n")



    def _connect_signals(self):
        self._view.calculate_btn.clicked.connect(self.calculate_button_actions)
        self._view.target_formula.returnPressed.connect(self.calculate_button_actions)
        self._view.optional_box.returnPressed.connect(self.calculate_button_actions)
        self._view.delete_logger_btn.clicked.connect(self._view.clear_data_list)

