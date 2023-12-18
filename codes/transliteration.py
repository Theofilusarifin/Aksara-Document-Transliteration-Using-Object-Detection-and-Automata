sandhangan_dict = {
    "taling" : 'e',
    "wulu" : 'i',
    "pepet" : 'è',
    "layar" : 'r',
    "cecak" : 'ng',
    "taling" : 'e',
    "suku" : 'u',
    "tarung" : 'o',
    "wignyan" : 'h',
    "lingsa" : ',',
    "lungsa" : '.',
}

sandhangan_pengubah_vokal = ["wulu", "pepet", "suku"]

sandhangan_awal = ["taling"]
sandhangan_atas = ["layar", "cecak"]
sandhangan_akhir = ["wignyan", "lingsa", "lungsa"]

class TransliterationFSA:
    def __init__(self):
        self.stored_taling = False
        self.result = ''
        self.temp_row_result = []

    def reset(self):
        self.stored_taling = False
        self.result = ''
        self.temp_row_result = []

    def process_input(self, jenis, aksara):
        try:
            if jenis == 'utama':
                self.q1(aksara)
            elif jenis == 'pasangan':
                self.q2(aksara)
            elif jenis == 'sandhangan':
                self.q3(aksara)
        except Exception as e:
            raise TransliterationFSAError(f"Error processing input: {e}")

    def q1(self, aksara):
        try:
            if self.stored_taling:
                self.temp_row_result.append(aksara[:-1] + 'e')
                self.stored_taling = False
            else:
                self.temp_row_result.append(aksara)
        except Exception as e:
            raise TransliterationFSAError(f"Error in q1: {e}")

    def q2(self, aksara):
        try:
            if self.stored_taling:
                self.temp_row_result.append(aksara[:-1] + 'e')
                self.stored_taling = False
            else:
                vokal_akhir = self.temp_row_result[-1][-1]
                if vokal_akhir != 'a':
                    if vokal_akhir == 'g':
                        vokal_akhir = self.temp_row_result[-1][-3:-1]
                        self.temp_row_result[-1] = self.temp_row_result[-1][:-3]
                    elif vokal_akhir in ('h', 'r'):
                        vokal_akhir = self.temp_row_result[-1][-2:-1]
                        self.temp_row_result[-1] = self.temp_row_result[-1][:-2]
                    else:
                        self.temp_row_result[-1] = self.temp_row_result[-1][:-1]
                    self.temp_row_result[-1] += aksara[:-1] + vokal_akhir
                else:
                    self.temp_row_result[-1] = self.temp_row_result[-1][:-1] + aksara
        except Exception as e:
            raise TransliterationFSAError(f"Error in q2: {e}")

    def q3(self, aksara):
        try:
            if self.temp_row_result:
                if aksara in sandhangan_pengubah_vokal:
                    self.temp_row_result[-1] = self.temp_row_result[-1][:-1] + sandhangan_dict[aksara]
                elif aksara in sandhangan_awal and "sandhangan_tarung" not in self.temp_row_result:
                    self.stored_taling = True
                elif aksara == 'tarung':
                    self.temp_row_result[-1] = self.temp_row_result[-1][:-1] + sandhangan_dict[aksara]
                elif aksara in sandhangan_atas or aksara in sandhangan_akhir:
                    self.temp_row_result[-1] += sandhangan_dict[aksara]
                elif aksara == "pangkon":
                    self.temp_row_result[-1] = self.temp_row_result[-1][:-1]
        except Exception as e:
            raise TransliterationFSAError(f"Error in q3: {e}")

    def get_result(self):
        return self.temp_row_result

class TransliterationFSAError(Exception):
    pass

def transliteration_fsa(pred_result):
    try:
        fsa = TransliterationFSA()
        final_result = []

        for selected_row in pred_result:
            try:
                row_result = []
                fsa.reset()

                for annotation in selected_row:
                    try:
                        jenis, aksara = annotation.split('_')
                        fsa.process_input(jenis, aksara)
                    except ValueError as ve:
                        raise FSAProcessError(f"Parsing annotation error: {ve}")

                row_result.extend(fsa.get_result())
                final_result.append(row_result)
            except Exception as e:
                raise FSAProcessError(f"Processing selected row error: {e}")

        return final_result
    except Exception as e:
        raise FSAProcessError(f"FSA Process error: {e}")

class FSAProcessError(Exception):
    pass
