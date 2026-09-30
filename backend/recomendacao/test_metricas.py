"""Testes de mrr_at_k e ground_truth_por_nota. Rode com: python -m unittest test_metrics -v"""

import unittest

from metricas import ground_truth_por_nota, mrr_at_k  


class TestMrrAtK(unittest.TestCase):
    def test_relevante_em_primeiro(self):
        self.assertEqual(mrr_at_k({1: [10, 20]}, {1: {10}}, k=5), 1.0)

    def test_relevante_em_terceiro(self):
        self.assertAlmostEqual(mrr_at_k({1: [1, 2, 10]}, {1: {10}}, k=5), 1 / 3)

    def test_fora_do_topk_vale_zero(self):
        self.assertEqual(mrr_at_k({1: [1, 2, 3, 4, 5, 6]}, {1: {6}}, k=5), 0.0)

    def test_ultimo_do_topk_conta(self):
        self.assertAlmostEqual(mrr_at_k({1: [1, 2, 3, 4, 6]}, {1: {6}}, k=5), 1 / 5)

    def test_duplicata_nao_desloca_posicao(self):
        self.assertAlmostEqual(mrr_at_k({1: [7, 7, 7, 9]}, {1: {9}}, k=5), 1 / 2)

    def test_usa_o_primeiro_relevante(self):
        self.assertAlmostEqual(mrr_at_k({1: [1, 5, 9]}, {1: {5, 9}}, k=5), 1 / 2)

    def test_media_entre_usuarios(self):
        rankings = {1: [10], 2: [1, 2]}
        verdade = {1: {10}, 2: {2}}
        self.assertAlmostEqual(mrr_at_k(rankings, verdade, k=5), 0.75)

    def test_usuario_sem_ground_truth_fora_por_padrao(self):
        self.assertEqual(mrr_at_k({1: [10], 2: [5]}, {1: {10}}, k=5), 1.0)

    def test_usuario_sem_ground_truth_entra_com_flag(self):
        valor = mrr_at_k({1: [10], 2: [5]}, {1: {10}}, k=5, incluir_usuarios_sem_ground_truth=True)
        self.assertAlmostEqual(valor, 0.5)

    def test_ranking_vazio_conta_zero(self):
        self.assertAlmostEqual(mrr_at_k({1: [10], 2: []}, {1: {10}, 2: {3}}, k=5), 0.5)

    def test_sem_usuarios_em_comum(self):
        self.assertEqual(mrr_at_k({1: [10]}, {2: {10}}, k=5), 0.0)

    def test_k_invalido(self):
        with self.assertRaises(ValueError):
            mrr_at_k({1: [10]}, {1: {10}}, k=0)


class TestGroundTruth(unittest.TestCase):
    def test_filtra_por_nota_minima(self):
        interacoes = [
            {"user_id": 1, "recipe_id": 10, "rating": 5},
            {"user_id": 1, "recipe_id": 11, "rating": 3},
            {"user_id": 2, "recipe_id": 12, "rating": 4},
        ]
        self.assertEqual(ground_truth_por_nota(interacoes, nota_minima=4), {1: {10}, 2: {12}})

    def test_chaves_customizadas(self):
        interacoes = [{"usuario_id": 1, "prato_id": 10, "nota": 4.5}]
        resultado = ground_truth_por_nota(
            interacoes, usuario_chave="usuario_id", item_chave="prato_id", nota_chave="nota"
        )
        self.assertEqual(resultado, {1: {10}})


if __name__ == "__main__":
    unittest.main()