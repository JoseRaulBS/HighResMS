from config import Config

class Model:
    def __init__(self):
        pass

    def process_formula(self, formula):

        weight = 0
        elements = self.count_elements(formula)
        for element in elements:
            try:
                element_weight = Config.element_weights[element[0]]
            except KeyError:
                return "Not found"

            element_count = element[1]
            weight += element_weight * element_count

        final_text_to_print = self.process_result(weight, formula)
        return final_text_to_print

    def process_result(self, weight, formula):
        sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        adduct_weight = self.get_adduct_weight(self.adduct)
        final_weight = weight - (Config.e_mass * self.charge) + adduct_weight

        if self.charge == 0:
            adduct_symbol = ""
        elif self.charge < 1:
            adduct_symbol = f"{(str(self.charge)[1:]).translate(sup)}⁻"
        elif self.charge == -1:
            adduct_symbol = "⁻"
        elif self.charge == 1:
            adduct_symbol = "⁺"
        else:
            adduct_symbol = f"{str(self.charge).translate(sup)}⁺"

        formula_to_print = self.make_up_formula(formula)

        if adduct_weight == 0:
            final_text_to_print = f"{formula_to_print}{adduct_symbol} -> {round(final_weight, 5)} u"
        elif adduct_weight != "":
            final_text_to_print = f"{formula_to_print} [{self.adduct}]{adduct_symbol} -> {round(final_weight, 5)} u"

        return final_text_to_print

    def make_up_formula(self, formula):
        sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

        new_formula = []
        for item in formula:
            if item.isnumeric():
                sub_number = item.translate(sub)
                new_formula.append(sub_number)
            else:
                new_formula.append(item)

        final_formula = (''.join([str(e) for e in new_formula]))

        return final_formula

    def count_elements(self, formula):
        elements = self.separate_formula(formula)

        counted_elements = []

        for element in elements:
            numberstartindex = len(element)
            index = 0
            for letter in element:
                if letter.isnumeric():
                    numberstartindex = index
                    break
                index += 1
            element_letters = element[:numberstartindex]
            element_count = element[numberstartindex:]
            if element_count == "":
                element_count = 1
            element_count = int(element_count)
            counted_elements.append([element_letters, element_count])
        return counted_elements

    def separate_formula(self, formula):
        elements = []
        curr_element = ""

        for letter in formula:

            if letter == " ":
                continue
            elif letter.isupper():
                elements.append(curr_element)
                curr_element = letter
            else:
                curr_element += letter
        elements.append(curr_element)
        elements = [x for x in elements if len(x) > 0]
        return elements

    def get_adduct_weight(self, adduct):
        adduct_weight = Config.adducts[str(adduct)]
        return adduct_weight


    def run_calculator(self, formula, charge, adduct):
        self.charge = charge
        self.adduct = adduct

        final_text_to_print = self.process_formula(formula)

        return final_text_to_print
