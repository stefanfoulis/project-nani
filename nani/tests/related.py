# -*- coding: utf-8 -*-
from nani.test_utils.context_managers import LanguageOverride
from nani.test_utils.testcase import SingleNormalTestCase, NaniTestCase
from testproject.app.models import Normal, Related, Standard


class NormalToNormalFKTest(SingleNormalTestCase):
    def test_relation(self):
        """
        'normal' (aka 'shared') relations are relations from the shared (or
        normal) model to another shared (or normal) model.
        
        They should behave like normal foreign keys in Django
        """
        normal = self.get_obj()
        related = Related.objects.create(normal=normal)
        self.assertEqual(related.normal.pk, normal.pk)
        self.assertEqual(related.normal.shared_field, normal.shared_field)
        self.assertEqual(related.normal.translated_field, normal.translated_field)
        self.assertTrue(related in normal.rel1.all())


class NormalToTransFKTest(SingleNormalTestCase):
    def test_relation(self):
        """
        TranslatedForeignKeys are FKs linking to a specific translation.
        
        While they are used the same way as normal FKs, they internally change
        their target model to the translation model.
        """
        en = self.get_obj()
        ja = en
        ja.language_code = 'ja'
        ja.translated_field = u'何'
        ja.save()
        self.assertEqual(Normal._meta.translations_model.objects.count(), 2)
        related = Related.objects.language('en').create(normal_trans=ja)
        with LanguageOverride('en'):
            related = self.reload(related)
            self.assertEqual(related.normal_trans.pk, ja.pk)
            self.assertEqual(related.normal_trans.shared_field, ja.shared_field)
            self.assertEqual(related.normal_trans.translated_field, ja.translated_field)
            self.assertTrue(related in ja.rel2.all())


class TransToNormalFKTest(NaniTestCase):
    pass


class TransToTransFKTest(NaniTestCase):
    pass


class StandardToTransFKTest(NaniTestCase):
    fixtures = ['standard.json']
    
    def test_relation(self):
        en = Normal.objects.language('en').get(pk=1)
        ja = Normal.objects.language('ja').get(pk=1)
        related = Standard.objects.get(pk=1)
        with LanguageOverride('en'):
            related = self.reload(related)
            self.assertEqual(related.normal.pk, en.pk)
            self.assertEqual(related.normal.shared_field, en.shared_field)
            self.assertEqual(related.normal.translated_field, en.translated_field)
            self.assertTrue(related in en.standards.all())
        with LanguageOverride('ja'):
            related = self.reload(related)
            self.assertEqual(related.normal.pk, ja.pk)
            self.assertEqual(related.normal.shared_field, ja.shared_field)
            self.assertEqual(related.normal.translated_field, ja.translated_field)
            self.assertTrue(related in ja.standards.all())
            
    def test_num_queries(self):
        with LanguageOverride('en'):
            en = Normal.objects.language('en').get(pk=1)
            with self.assertNumQueries(1):
                related = Standard.objects.select_related('normal').get(pk=1)
                self.assertEqual(related.normal.pk, en.pk)
                self.assertEqual(related.normal.shared_field, en.shared_field)
                self.assertEqual(related.normal.translated_field, en.translated_field)

    def test_lookup_by_pk(self):
        en = Normal.objects.language('en').get(pk=1)
        by_pk = Standard.objects.get(normal__pk=en.pk)
        with LanguageOverride('en'):
            self.assertEqual(by_pk.normal.pk, en.pk)
            self.assertEqual(by_pk.normal.shared_field, en.shared_field)
            self.assertEqual(by_pk.normal.translated_field, en.translated_field)
            self.assertTrue(by_pk in en.standards.all())
            
    def test_lookup_by_shared_field(self):
        en = Normal.objects.language('en').get(pk=1)
        by_shared_field = Standard.objects.get(normal__shared_field=en.shared_field)
        with LanguageOverride('en'):
            self.assertEqual(by_shared_field.normal.pk, en.pk)
            self.assertEqual(by_shared_field.normal.shared_field, en.shared_field)
            self.assertEqual(by_shared_field.normal.translated_field, en.translated_field)
            self.assertTrue(by_shared_field in en.standards.all())
    
    def test_lookup_by_translated_field(self):
        en = Normal.objects.language('en').get(pk=1)
        by_translated_field = Standard.objects.get(normal__translated_field=en.translated_field)
        with LanguageOverride('en'):
            self.assertEqual(by_translated_field.normal.pk, en.pk)
            self.assertEqual(by_translated_field.normal.shared_field, en.shared_field)
            self.assertEqual(by_translated_field.normal.translated_field, en.translated_field)
            self.assertTrue(by_translated_field in en.standards.all())