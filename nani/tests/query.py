# -*- coding: utf-8 -*-
from nani.test_utils.context_managers import LanguageOverride
from nani.test_utils.data import DOUBLE_NORMAL
from nani.test_utils.testcase import NaniTestCase
from testproject.app.models import Normal


class FilterTests(NaniTestCase):
    fixtures = ['double_normal.json']
    
    def test_simple_filter(self):
        qs = Normal.objects.language('en').filter(shared_field__contains='2')
        self.assertEqual(qs.count(), 1)
        obj = qs[0]
        self.assertEqual(obj.shared_field, DOUBLE_NORMAL[2]['shared_field'])
        self.assertEqual(obj.translated_field, DOUBLE_NORMAL[2]['translated_field_en'])
        qs = Normal.objects.language('ja').filter(shared_field__contains='1')
        self.assertEqual(qs.count(), 1)
        obj = qs[0]
        self.assertEqual(obj.shared_field, DOUBLE_NORMAL[1]['shared_field'])
        self.assertEqual(obj.translated_field, DOUBLE_NORMAL[1]['translated_field_ja'])
        
    def test_translated_filter(self):
        qs = Normal.objects.filter(translated_field__contains='English')
        self.assertEqual(qs.count(), 2)
        obj1, obj2 = qs
        self.assertEqual(obj1.shared_field, DOUBLE_NORMAL[1]['shared_field'])
        self.assertEqual(obj1.translated_field, DOUBLE_NORMAL[1]['translated_field_en'])
        self.assertEqual(obj2.shared_field, DOUBLE_NORMAL[2]['shared_field'])
        self.assertEqual(obj2.translated_field, DOUBLE_NORMAL[2]['translated_field_en'])


class IterTests(NaniTestCase):
    fixtures = ['double_normal.json']
    
    def test_simple_iter(self):
        with LanguageOverride('en'):
            with self.assertNumQueries(1):
                index = 0
                for obj in Normal.objects.language():
                    index += 1
                    self.assertEqual(obj.shared_field, DOUBLE_NORMAL[index]['shared_field'])
                    self.assertEqual(obj.translated_field, DOUBLE_NORMAL[index]['translated_field_en'])
        with LanguageOverride('ja'):
            with self.assertNumQueries(1):
                index = 0
                for obj in Normal.objects.language():
                    index += 1
                    self.assertEqual(obj.shared_field, DOUBLE_NORMAL[index]['shared_field'])
                    self.assertEqual(obj.translated_field, DOUBLE_NORMAL[index]['translated_field_ja'])

class UpdateTests(NaniTestCase):
    fixtures = ['double_normal.json']
    
    def test_update_shared(self):
        NEW_SHARED = 'new shared'
        n1 = Normal.objects.language('en').get(pk=1)
        n2 = Normal.objects.language('en').get(pk=2)
        ja1 = Normal.objects.language('ja').get(pk=1)
        ja2 = Normal.objects.language('ja').get(pk=2)
        with self.assertNumQueries(1):
            Normal.objects.language('en').update(shared_field=NEW_SHARED)
        new1 = Normal.objects.language('en').get(pk=1)
        new2 = Normal.objects.language('en').get(pk=2)
        self.assertEqual(new1.shared_field, NEW_SHARED)
        self.assertEqual(new1.translated_field, n1.translated_field)
        self.assertEqual(new2.shared_field, NEW_SHARED)
        self.assertEqual(new2.translated_field, n2.translated_field)
        newja1 = Normal.objects.language('ja').get(pk=1)
        newja2 = Normal.objects.language('ja').get(pk=2)
        self.assertEqual(newja1.shared_field, NEW_SHARED)
        self.assertEqual(newja2.shared_field, NEW_SHARED)
        self.assertEqual(newja1.translated_field, ja1.translated_field)
        self.assertEqual(newja2.translated_field, ja2.translated_field)
        
    def test_update_translated(self):
        NEW_TRANSLATED = 'new translated'
        n1 = Normal.objects.language('en').get(pk=1)
        n2 = Normal.objects.language('en').get(pk=2)
        ja1 = Normal.objects.language('ja').get(pk=1)
        ja2 = Normal.objects.language('ja').get(pk=2)
        with self.assertNumQueries(1):
            Normal.objects.language('en').update(translated_field=NEW_TRANSLATED)
        new1 = Normal.objects.language('en').get(pk=1)
        new2 = Normal.objects.language('en').get(pk=2)
        self.assertEqual(new1.shared_field, n1.shared_field)
        self.assertEqual(new2.shared_field, n2.shared_field)
        self.assertEqual(new1.translated_field, NEW_TRANSLATED)
        self.assertEqual(new2.translated_field, NEW_TRANSLATED)
        # check it didn't touch japanese
        newja1 = Normal.objects.language('ja').get(pk=1)
        newja2 = Normal.objects.language('ja').get(pk=2)
        self.assertEqual(newja1.shared_field, ja1.shared_field)
        self.assertEqual(newja2.shared_field, ja2.shared_field)
        self.assertEqual(newja1.translated_field, ja1.translated_field)
        self.assertEqual(newja2.translated_field, ja2.translated_field)
        
    def test_update_mixed(self):
        NEW_SHARED = 'new shared'
        NEW_TRANSLATED = 'new translated'
        ja1 = Normal.objects.language('ja').get(pk=1)
        ja2 = Normal.objects.language('ja').get(pk=2)
        with self.assertNumQueries(2):
            Normal.objects.language('en').update(shared_field=NEW_SHARED, translated_field=NEW_TRANSLATED)
        new1 = Normal.objects.language('en').get(pk=1)
        new2 = Normal.objects.language('en').get(pk=2)
        self.assertEqual(new1.shared_field, NEW_SHARED)
        self.assertEqual(new1.translated_field, NEW_TRANSLATED)
        self.assertEqual(new2.shared_field, NEW_SHARED)
        self.assertEqual(new2.translated_field, NEW_TRANSLATED)
        newja1 = Normal.objects.language('ja').get(pk=1)
        newja2 = Normal.objects.language('ja').get(pk=2)
        self.assertEqual(newja1.shared_field, NEW_SHARED)
        self.assertEqual(newja2.shared_field, NEW_SHARED)
        # check it didn't touch japanese translated fields
        self.assertEqual(newja1.translated_field, ja1.translated_field)
        self.assertEqual(newja2.translated_field, ja2.translated_field)
        

class ValuesListTests(NaniTestCase):
    fixtures = ['double_normal.json']
    
    def test_values_list_translated(self):
        values = Normal.objects.language('en').values_list('translated_field', flat=True)
        values_list = list(values)
        self.assertEqual(values_list, [DOUBLE_NORMAL[1]['translated_field_en'], DOUBLE_NORMAL[2]['translated_field_en']])
        
    def test_values_list_shared(self):
        values = Normal.objects.language('en').values_list('shared_field', flat=True)
        values_list = list(values)
        self.assertEqual(values_list, [DOUBLE_NORMAL[1]['shared_field'], DOUBLE_NORMAL[2]['shared_field']])
    
    def test_values_list_mixed(self):
        values = Normal.objects.language('en').values_list('shared_field', 'translated_field')
        values_list = list(values)
        check = [
            (DOUBLE_NORMAL[1]['shared_field'], DOUBLE_NORMAL[1]['translated_field_en']),
            (DOUBLE_NORMAL[2]['shared_field'], DOUBLE_NORMAL[2]['translated_field_en']),
        ]
        self.assertEqual(values_list, check)
        

class ValuesTests(NaniTestCase):
    fixtures = ['double_normal.json']
    
    def test_values_shared(self):
        values = Normal.objects.language('en').values('shared_field')
        values_list = list(values)
        check = [
            {'shared_field': DOUBLE_NORMAL[1]['shared_field']},
            {'shared_field': DOUBLE_NORMAL[2]['shared_field']},
        ]
        self.assertEqual(values_list, check)
    
    def test_values_translated(self):
        values = Normal.objects.language('en').values('translated_field')
        values_list = list(values)
        check = [
            {'translated_field': DOUBLE_NORMAL[1]['translated_field_en']},
            {'translated_field': DOUBLE_NORMAL[2]['translated_field_en']},
        ]
        self.assertEqual(values_list, check)
        
    def test_values_mixed(self):
        values = Normal.objects.language('en').values('translated_field', 'shared_field')
        values_list = list(values)
        check = [
            {'translated_field': DOUBLE_NORMAL[1]['translated_field_en'],
             'shared_field': DOUBLE_NORMAL[1]['shared_field']},
            {'translated_field': DOUBLE_NORMAL[2]['translated_field_en'],
             'shared_field': DOUBLE_NORMAL[2]['shared_field']},
        ]
        self.assertEqual(values_list, check)
        
    def test_values_post_language(self):
        values = Normal.objects.values('shared_field').language('en')
        values_list = list(values)
        check = [
            {'shared_field': DOUBLE_NORMAL[1]['shared_field']},
            {'shared_field': DOUBLE_NORMAL[2]['shared_field']},
        ]
        self.assertEqual(values_list, check)
        
    def test_values_post_filter(self):
        qs = Normal.objects.language('en').values('shared_field')
        values = qs.filter(shared_field=DOUBLE_NORMAL[1]['shared_field'])
        values_list = list(values)
        check = [
            {'shared_field': DOUBLE_NORMAL[1]['shared_field']},
        ]
        self.assertEqual(values_list, check)
        

class DeleteTests(NaniTestCase):
    fixtures = ['double_normal.json']
    
    def test_delete_all(self):
        Normal.objects.all().delete()
        self.assertEqual(Normal.objects.count(), 0)
        self.assertEqual(Normal.objects._real_manager.count(), 0)
        self.assertEqual(Normal._meta.translations_model.objects.count(), 0)
        
    def test_delete_translation(self):
        Normal.objects.language('en').delete_translations()
        self.assertEqual(Normal.objects.count(), 2)
        self.assertEqual(Normal.objects._real_manager.count(), 2)
        self.assertEqual(Normal._meta.translations_model.objects.count(), 2)