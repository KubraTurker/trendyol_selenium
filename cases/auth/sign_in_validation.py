# Kullanici login olabiliyor mu kontrolu yapilir
# 1. Ana sayfaya gidilir
# 2. Login Butonuna tiklanir
# 3. Bilgiler bos birakilir
# 4. Validasyon hatasi dogrulanir
import unittest

from generic import initialize, auth


class TestUserLoginValidation(unittest.TestCase):

    def setUp(self):
        """Tarayıcı başlatılır ve test için hazırlanır."""
        print("\n🔄 Tarayıcı başlatılıyor...")
        self.driver = initialize.run()

