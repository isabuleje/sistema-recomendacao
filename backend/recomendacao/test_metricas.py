import unittest

from .metricas import ground_truth_por_nota, mrr_at_k


class MrrAtKTests(unittest.TestCase):
    def test_item_relevante_na_primeira_posicao(self):
        self.assertEqual(mrr_at_k({1: [10, 20]}, {1: {10}}), 1.0)

    def test_item_relevante_nas_posicoes_2_e_5(self):
        resultado = mrr_at_k(
            {1: [10, 20], 2: [10, 11, 12, 13, 14]},
            {1: {20}, 2: {14}},
        )
        self.assertAlmostEqual(resultado, (1 / 2 + 1 / 5) / 2)

    def test_usuario_sem_item_relevante_recebe_zero(self):
        self.assertEqual(mrr_at_k({1: [10, 20]}, {1: {30}}), 0.0)

    def test_ranking_menor_que_k(self):
        self.assertEqual(mrr_at_k({1: [10, 20]}, {1: {20}}), 0.5)

    def test_usuario_sem_ground_truth_e_ignorado_por_padrao(self):
        self.assertEqual(mrr_at_k({1: [10], 2: [20]}, {1: {10}}), 1.0)

    def test_usuario_sem_ground_truth_pode_receber_zero(self):
        self.assertEqual(
            mrr_at_k(
                {1: [10], 2: [20]},
                {1: {10}},
                incluir_usuarios_sem_ground_truth=True,
            ),
            0.5,
        )

    def test_entradas_vazias(self):
        self.assertEqual(mrr_at_k({}, {}), 0.0)

    def test_duplicatas_nao_inflam_o_resultado(self):
        self.assertEqual(mrr_at_k({1: [10, 10, 20]}, {1: {20}}), 0.5)

    def test_ground_truth_usa_nota_minima_4(self):
        interacoes = [
            {"user_id": 1, "recipe_id": 10, "rating": 3},
            {"user_id": 1, "recipe_id": 20, "rating": 4},
        ]
        self.assertEqual(ground_truth_por_nota(interacoes), {1: {20}})


if __name__ == "__main__":
    unittest.main()