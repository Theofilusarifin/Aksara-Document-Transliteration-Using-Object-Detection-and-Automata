sandhangan_dict = {
    "taling": 'e',
    "wulu": 'i',
    "pepet": 'è',
    "layar": 'r',
    "cecak": 'ng',
    "taling": 'e',
    "suku": 'u',
    "tarung": 'o',
    "wignyan": 'h',
    "lingsa": ',',
    "lungsa": '.',
}

sandhangan_pengubah_vokal = ["wulu", "pepet", "suku"]

sandhangan_awal = ["taling"]
sandhangan_atas = ["layar", "cecak"]
sandhangan_akhir = ["wignyan", "lingsa", "lungsa"]


class TransliterationDFA:
    def __init__(self):
        self.stored_taling = False
        self.result = ''

    def reset(self):
        self.stored_taling = False
        self.result = ''

    def process_input(self, jenis, aksara):
        if jenis == 'utama':
            self.q1(aksara)
        elif jenis == 'pasangan':
            self.q2(aksara)
        elif jenis == 'sandhangan':
            self.q3(aksara)

    def q1(self, aksara):
        # Function rules untuk carakan
        if self.stored_taling:
            self.result += aksara[:-1] + 'e'
            self.stored_taling = False
        else:
            self.result += aksara

    def q2(self, aksara):
        # Function rules untuk pasangan
        if self.stored_taling:
            self.result += aksara[:-1] + 'e'
            self.stored_taling = False
        else:
            vokal_akhir = self.result[-1]
            if vokal_akhir != 'a':
                if vokal_akhir == 'g':
                    vokal_akhir = self.result[-3:-1]
                    self.result = self.result[:-3]
                elif vokal_akhir in ('h', 'r'):
                    vokal_akhir = self.result[-2:-1]
                    self.result = self.result[:-2]
                else:
                    self.result = self.result[:-1]
                self.result += aksara[:-1] + vokal_akhir
            else:
                self.result = self.result[:-1] + aksara

    def q3(self, aksara):
        # Function rules untuk sandhangan
        if aksara in sandhangan_pengubah_vokal:
            self.result = self.result[:-1] + sandhangan_dict[aksara]
        elif aksara in sandhangan_awal and "sandhangan_tarung" not in self.result:
            self.stored_taling = True
        elif aksara == 'tarung':
            self.result = self.result[:-1] + sandhangan_dict[aksara]
        elif aksara in sandhangan_atas or aksara in sandhangan_akhir:
            self.result += sandhangan_dict[aksara]
        elif aksara == "pangkon":
            self.result = self.result[:-1]

    def get_result(self):
        return self.result


def transliteration_dfa(pred_result):
    dfa = TransliterationDFA()
    final_result = []

    for selected_row in pred_result:
        row_result = []
        dfa.reset()

        for annotation in selected_row:
            jenis, aksara = annotation.split('_')
            dfa.process_input(jenis, aksara)

        row_result.append(dfa.get_result())
        final_result.append(row_result)

    return final_result