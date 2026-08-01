/* ==========================================================================
   Blinkit Quick Commerce MVP - Complete Mock Database Store (50+ Items)
   ========================================================================== */

// Helper to generate SVG Data URIs for crisp product visuals
const createProductSVG = (bgColor, emoji, label) => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
    <rect width="200" height="200" fill="${bgColor}" rx="16"/>
    <text x="50%" y="45%" dominant-baseline="central" text-anchor="middle" font-size="70">${emoji}</text>
    <text x="50%" y="80%" dominant-baseline="central" text-anchor="middle" font-size="13" font-family="sans-serif" font-weight="bold" fill="#334155">${label}</text>
  </svg>`;
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
};

export const MOCK_DATA = {
  categories: [
    { id: 'cat-all', name: 'All Products', icon: '🛒', slug: 'all' },
    { id: 'cat-veg', name: 'Vegetables & Fruits', icon: '🥦', slug: 'veg-fruits' },
    { id: 'cat-dairy', name: 'Dairy & Bread', icon: '🥛', slug: 'dairy-bread' },
    { id: 'cat-drinks', name: 'Cold Drinks & Juices', icon: '🥤', slug: 'drinks-juices' },
    { id: 'cat-snacks', name: 'Snacks & Munchies', icon: '🍟', slug: 'snacks-munchies' },
    { id: 'cat-instant', name: 'Instant Food', icon: '🍜', slug: 'instant-food' },
    { id: 'cat-cleaning', name: 'Cleaning & Household', icon: '🧹', slug: 'cleaning-household' },
    { id: 'cat-personal', name: 'Personal Care', icon: '🧴', slug: 'personal-care' }
  ],

  darkStores: [
    {
      id: 'ds-104',
      code: 'DS-IND-104',
      name: 'Dark Store #104 - Indiranagar',
      address: 'Plot 42, 100 Feet Rd, Indiranagar, Bengaluru',
      lat: 12.971598,
      lng: 77.594566,
      radiusKm: 2.5,
      active: true
    },
    {
      id: 'ds-102',
      code: 'DS-KOR-102',
      name: 'Dark Store #102 - Koramangala',
      address: '80 Feet Rd, 4th Block, Koramangala, Bengaluru',
      lat: 12.935242,
      lng: 77.624462,
      radiusKm: 3.0,
      active: true
    },
    {
      id: 'ds-108',
      code: 'DS-HSR-108',
      name: 'Dark Store #108 - HSR Layout',
      address: '27th Main Rd, Sector 1, HSR Layout, Bengaluru',
      lat: 12.912118,
      lng: 77.644554,
      radiusKm: 2.5,
      active: true
    }
  ],

  riders: [
    {
      id: 'r-101',
      name: 'Ramesh Kumar',
      phone: '+91 98765 43210',
      vehicle: 'EV Scooter (KA-01-EQ-4492)',
      status: 'IDLE',
      darkStoreId: 'ds-104',
      avatar: '🛵'
    },
    {
      id: 'r-102',
      name: 'Suresh Patil',
      phone: '+91 98123 45678',
      vehicle: 'EV Scooter (KA-05-EV-1120)',
      status: 'IDLE',
      darkStoreId: 'ds-104',
      avatar: '🛵'
    },
    {
      id: 'r-103',
      name: 'Vikram Singh',
      phone: '+91 97788 99001',
      vehicle: 'Electric Bike (KA-03-EB-8821)',
      status: 'IDLE',
      darkStoreId: 'ds-102',
      avatar: '⚡'
    },
    {
      id: 'r-104',
      name: 'Anil Verma',
      phone: '+91 98222 33445',
      vehicle: 'EV Scooter (KA-04-EV-9901)',
      status: 'IDLE',
      darkStoreId: 'ds-108',
      avatar: '🛵'
    },
    {
      id: 'r-105',
      name: 'Deepak Gowda',
      phone: '+91 99112 23344',
      vehicle: 'Electric Bike (KA-01-EB-1234)',
      status: 'IDLE',
      darkStoreId: 'ds-104',
      avatar: '⚡'
    }
  ],

  userAddresses: [
    {
      id: 'addr-1',
      label: 'Home',
      street: '104 Park View Apartments, 12th Main, Indiranagar',
      landmark: 'Near 100ft Road Metro Station',
      lat: 12.972500,
      lng: 77.595000,
      isDefault: true
    },
    {
      id: 'addr-2',
      label: 'Work',
      street: 'Tech Park Tower 4B, 5th Floor, Koramangala',
      landmark: 'Opposite Forum Mall',
      lat: 12.936000,
      lng: 77.625000,
      isDefault: false
    }
  ],

  products: [
    // --- 1. Vegetables & Fruits (10 Items) ---
    {
      id: 'p-101',
      categoryId: 'cat-veg',
      title: 'Fresh Farm Tomatoes',
      unit: '500 g',
      mrp: 35,
      price: 24,
      image: './src/assets/images/fresh_produce.png',
      rack: 'Aisle 1 • Shelf A1',
      tags: ['fresh', 'organic', 'vegetables', 'tomatoes'],
      stock: 45
    },
    {
      id: 'p-102',
      categoryId: 'cat-veg',
      title: 'Robusta Bananas',
      unit: '1 kg (6-7 pcs)',
      mrp: 60,
      price: 48,
      image: createProductSVG('#fef08a', '🍌', 'Bananas'),
      rack: 'Aisle 1 • Shelf A2',
      tags: ['fruit', 'potassium', 'banana'],
      stock: 30
    },
    {
      id: 'p-103',
      categoryId: 'cat-veg',
      title: 'Fresh Broccoli',
      unit: '1 pc (250-300g)',
      mrp: 75,
      price: 55,
      image: createProductSVG('#bbf7d0', '🥦', 'Broccoli'),
      rack: 'Aisle 1 • Shelf B1',
      tags: ['green', 'broccoli', 'exotic'],
      stock: 18
    },
    {
      id: 'p-104',
      categoryId: 'cat-veg',
      title: 'Shimla Red Apples',
      unit: '4 pcs (approx 500g)',
      mrp: 140,
      price: 119,
      image: createProductSVG('#fecaca', '🍎', 'Apples'),
      rack: 'Aisle 1 • Shelf B2',
      tags: ['fresh', 'fruit', 'apple'],
      stock: 25
    },
    {
      id: 'p-105',
      categoryId: 'cat-veg',
      title: 'Organic Spinach (Palak)',
      unit: '1 Bunch (200g)',
      mrp: 30,
      price: 19,
      image: createProductSVG('#dcfce7', '🥬', 'Spinach'),
      rack: 'Aisle 1 • Shelf C1',
      tags: ['leafy', 'palak', 'spinach'],
      stock: 40
    },
    {
      id: 'p-106',
      categoryId: 'cat-veg',
      title: 'Hybrid Onions',
      unit: '1 kg',
      mrp: 45,
      price: 34,
      image: createProductSVG('#e9d5ff', '🧅', 'Onions'),
      rack: 'Aisle 1 • Shelf C2',
      tags: ['onions', 'vegetables', 'staple'],
      stock: 60
    },
    {
      id: 'p-107',
      categoryId: 'cat-veg',
      title: 'Fresh Potatoes',
      unit: '1 kg',
      mrp: 40,
      price: 29,
      image: createProductSVG('#fef08a', '🥔', 'Potatoes'),
      rack: 'Aisle 1 • Shelf D1',
      tags: ['potatoes', 'aloo', 'vegetables'],
      stock: 75
    },
    {
      id: 'p-108',
      categoryId: 'cat-veg',
      title: 'Green Capsicum (Bell Pepper)',
      unit: '250 g',
      mrp: 38,
      price: 28,
      image: createProductSVG('#bbf7d0', '🫑', 'Capsicum'),
      rack: 'Aisle 1 • Shelf D2',
      tags: ['capsicum', 'pepper', 'green'],
      stock: 22
    },
    {
      id: 'p-109',
      categoryId: 'cat-veg',
      title: 'Fresh Alphonso Mangoes',
      unit: '2 pcs (approx 500g)',
      mrp: 220,
      price: 189,
      image: createProductSVG('#fed7aa', '🥭', 'Mangoes'),
      rack: 'Aisle 1 • Shelf E1',
      tags: ['mango', 'fruit', 'sweet'],
      stock: 15
    },
    {
      id: 'p-110',
      categoryId: 'cat-veg',
      title: 'Organic Carrots',
      unit: '500 g',
      mrp: 45,
      price: 32,
      image: createProductSVG('#ffedd5', '🥕', 'Carrots'),
      rack: 'Aisle 1 • Shelf E2',
      tags: ['carrot', 'orange', 'gajar'],
      stock: 35
    },

    // --- 2. Dairy & Bread (8 Items) ---
    {
      id: 'p-201',
      categoryId: 'cat-dairy',
      title: 'Amul Taaza Toned Milk',
      unit: '500 ml',
      mrp: 27,
      price: 27,
      image: './src/assets/images/dairy_bakery.png',
      rack: 'Cold Refrigerator #1',
      tags: ['milk', 'dairy', 'amul'],
      stock: 80
    },
    {
      id: 'p-202',
      categoryId: 'cat-dairy',
      title: 'Modern Whole Wheat Bread',
      unit: '400 g',
      mrp: 50,
      price: 45,
      image: createProductSVG('#fde68a', '🍞', 'Brown Bread'),
      rack: 'Aisle 2 • Shelf A1',
      tags: ['bread', 'breakfast', 'wheat'],
      stock: 35
    },
    {
      id: 'p-203',
      categoryId: 'cat-dairy',
      title: 'Amul Pasteurised Butter',
      unit: '100 g',
      mrp: 60,
      price: 58,
      image: createProductSVG('#fef08a', '🧈', 'Butter'),
      rack: 'Cold Refrigerator #2',
      tags: ['butter', 'dairy', 'amul'],
      stock: 50
    },
    {
      id: 'p-204',
      categoryId: 'cat-dairy',
      title: 'Farm Fresh White Eggs',
      unit: '1 Tray (6 pcs)',
      mrp: 55,
      price: 46,
      image: createProductSVG('#f3f4f6', '🥚', 'Eggs (6 Pcs)'),
      rack: 'Aisle 2 • Shelf B2',
      tags: ['protein', 'breakfast', 'eggs'],
      stock: 60
    },
    {
      id: 'p-205',
      categoryId: 'cat-dairy',
      title: 'Fresh Malai Paneer',
      unit: '200 g',
      mrp: 95,
      price: 85,
      image: createProductSVG('#ffffff', '🧀', 'Paneer'),
      rack: 'Cold Refrigerator #1',
      tags: ['paneer', 'cottage cheese'],
      stock: 22
    },
    {
      id: 'p-206',
      categoryId: 'cat-dairy',
      title: 'Amul Masti Dahi (Curd)',
      unit: '400 g Pouch',
      mrp: 35,
      price: 35,
      image: createProductSVG('#e2e8f0', '🥣', 'Curd / Dahi'),
      rack: 'Cold Refrigerator #2',
      tags: ['dahi', 'curd', 'amul'],
      stock: 45
    },
    {
      id: 'p-207',
      categoryId: 'cat-dairy',
      title: 'Britannia Cheese Slices',
      unit: '200 g (10 Slices)',
      mrp: 155,
      price: 139,
      image: createProductSVG('#fef08a', '🧀', 'Cheese Slices'),
      rack: 'Cold Refrigerator #2',
      tags: ['cheese', 'britannia', 'slices'],
      stock: 28
    },
    {
      id: 'p-208',
      categoryId: 'cat-dairy',
      title: 'Epigamia Greek Yogurt (Mango)',
      unit: '85 g',
      mrp: 50,
      price: 45,
      image: createProductSVG('#fed7aa', '🍨', 'Greek Yogurt'),
      rack: 'Cold Refrigerator #3',
      tags: ['yogurt', 'epigamia', 'greek'],
      stock: 30
    },

    // --- 3. Cold Drinks & Juices (8 Items) ---
    {
      id: 'p-301',
      categoryId: 'cat-drinks',
      title: 'Coca-Cola Soft Drink Can',
      unit: '300 ml',
      mrp: 40,
      price: 38,
      image: createProductSVG('#fca5a5', '🥤', 'Coca-Cola'),
      rack: 'Cold Beverage Rack #1',
      tags: ['cola', 'cold drink', 'soda'],
      stock: 100
    },
    {
      id: 'p-302',
      categoryId: 'cat-drinks',
      title: 'Real Fruit Power Orange Juice',
      unit: '1 Liter',
      mrp: 130,
      price: 110,
      image: createProductSVG('#fed7aa', '🍊', 'Orange Juice'),
      rack: 'Cold Beverage Rack #2',
      tags: ['juice', 'orange', 'real'],
      stock: 40
    },
    {
      id: 'p-303',
      categoryId: 'cat-drinks',
      title: 'Red Bull Energy Drink',
      unit: '250 ml',
      mrp: 125,
      price: 115,
      image: createProductSVG('#bfdbfe', '⚡', 'Red Bull'),
      rack: 'Cold Beverage Rack #1',
      tags: ['energy', 'drink', 'redbull'],
      stock: 35
    },
    {
      id: 'p-304',
      categoryId: 'cat-drinks',
      title: 'Sprite Lime Soft Drink',
      unit: '750 ml Bottle',
      mrp: 45,
      price: 40,
      image: createProductSVG('#bbf7d0', '🍾', 'Sprite 750ml'),
      rack: 'Cold Beverage Rack #2',
      tags: ['sprite', 'lime', 'soda'],
      stock: 55
    },
    {
      id: 'p-305',
      categoryId: 'cat-drinks',
      title: 'Tropicana 100% Mixed Fruit Juice',
      unit: '1 Liter',
      mrp: 145,
      price: 125,
      image: createProductSVG('#fed7aa', '🧃', 'Mixed Juice'),
      rack: 'Cold Beverage Rack #3',
      tags: ['juice', 'tropicana', 'mixed fruit'],
      stock: 25
    },
    {
      id: 'p-306',
      categoryId: 'cat-drinks',
      title: 'Bisleri Packed Mineral Water',
      unit: '1 Liter',
      mrp: 20,
      price: 20,
      image: createProductSVG('#e0f2fe', '💧', 'Bisleri Water'),
      rack: 'Cold Beverage Rack #3',
      tags: ['water', 'bisleri', 'mineral'],
      stock: 150
    },
    {
      id: 'p-307',
      categoryId: 'cat-drinks',
      title: 'Paper Boat Tender Coconut Water',
      unit: '200 ml',
      mrp: 50,
      price: 45,
      image: createProductSVG('#dcfce7', '🥥', 'Coconut Water'),
      rack: 'Cold Beverage Rack #2',
      tags: ['coconut', 'paperboat', 'fresh'],
      stock: 40
    },
    {
      id: 'p-308',
      categoryId: 'cat-drinks',
      title: 'Amul Kool Chocolate Milk',
      unit: '200 ml Bottle',
      mrp: 30,
      price: 30,
      image: createProductSVG('#d97706', '🥛', 'Chocolate Milk'),
      rack: 'Cold Beverage Rack #1',
      tags: ['chocolate', 'milk', 'kool'],
      stock: 48
    },

    // --- 4. Snacks & Munchies (8 Items) ---
    {
      id: 'p-401',
      categoryId: 'cat-snacks',
      title: 'Lay’s Magic Masala Potato Chips',
      unit: '50 g',
      mrp: 20,
      price: 20,
      image: createProductSVG('#fef08a', '🍟', 'Lays Chips'),
      rack: 'Aisle 3 • Shelf A1',
      tags: ['chips', 'snack', 'lays'],
      stock: 120
    },
    {
      id: 'p-402',
      categoryId: 'cat-snacks',
      title: 'Doritos Nacho Cheese Chips',
      unit: '82.5 g',
      mrp: 50,
      price: 45,
      image: createProductSVG('#fbcfe8', '📐', 'Doritos'),
      rack: 'Aisle 3 • Shelf A2',
      tags: ['nachos', 'cheese', 'doritos'],
      stock: 65
    },
    {
      id: 'p-403',
      categoryId: 'cat-snacks',
      title: 'Haldiram’s Bhujia Sev',
      unit: '200 g',
      mrp: 65,
      price: 59,
      image: createProductSVG('#fed7aa', '🥨', 'Bhujia Sev'),
      rack: 'Aisle 3 • Shelf B1',
      tags: ['namkeen', 'sev', 'haldiram'],
      stock: 45
    },
    {
      id: 'p-404',
      categoryId: 'cat-snacks',
      title: 'Kurkure Masala Munch',
      unit: '85 g',
      mrp: 20,
      price: 20,
      image: createProductSVG('#fed7aa', '🌶️', 'Kurkure'),
      rack: 'Aisle 3 • Shelf B2',
      tags: ['kurkure', 'masala', 'snack'],
      stock: 90
    },
    {
      id: 'p-405',
      categoryId: 'cat-snacks',
      title: 'Pringles Original Potato Chips',
      unit: '107 g Can',
      mrp: 115,
      price: 99,
      image: createProductSVG('#fca5a5', '🥔', 'Pringles Can'),
      rack: 'Aisle 3 • Shelf C1',
      tags: ['pringles', 'chips', 'can'],
      stock: 30
    },
    {
      id: 'p-406',
      categoryId: 'cat-snacks',
      title: 'Act II Butter Popcorn (Microwave)',
      unit: '99 g',
      mrp: 45,
      price: 39,
      image: createProductSVG('#fef08a', '🍿', 'Popcorn'),
      rack: 'Aisle 3 • Shelf C2',
      tags: ['popcorn', 'act2', 'butter'],
      stock: 40
    },
    {
      id: 'p-407',
      categoryId: 'cat-snacks',
      title: 'Cadbury Dairy Milk Silk (Chocolate)',
      unit: '60 g',
      mrp: 80,
      price: 75,
      image: createProductSVG('#c084fc', '🍫', 'Dairy Milk Silk'),
      rack: 'Aisle 3 • Shelf D1',
      tags: ['chocolate', 'cadbury', 'silk'],
      stock: 50
    },
    {
      id: 'p-408',
      categoryId: 'cat-snacks',
      title: 'Nutraj California Almonds (Badam)',
      unit: '200 g',
      mrp: 250,
      price: 199,
      image: createProductSVG('#ffedd5', '🥜', 'Almonds'),
      rack: 'Aisle 3 • Shelf D2',
      tags: ['nuts', 'almonds', 'badam'],
      stock: 25
    },

    // --- 5. Instant Food (8 Items) ---
    {
      id: 'p-501',
      categoryId: 'cat-instant',
      title: 'Maggi 2-Minute Masala Noodles',
      unit: 'Pack of 4 (280g)',
      mrp: 56,
      price: 54,
      image: createProductSVG('#fef08a', '🍜', 'Maggi 4-Pack'),
      rack: 'Aisle 4 • Shelf A1',
      tags: ['maggi', 'noodles', 'instant'],
      stock: 90
    },
    {
      id: 'p-502',
      categoryId: 'cat-instant',
      title: 'Knorr Classic Tomato Soup',
      unit: '53 g',
      mrp: 60,
      price: 52,
      image: createProductSVG('#fecaca', '🍲', 'Tomato Soup'),
      rack: 'Aisle 4 • Shelf A2',
      tags: ['soup', 'knorr', 'tomato'],
      stock: 30
    },
    {
      id: 'p-503',
      categoryId: 'cat-instant',
      title: 'Yippee! Magic Masala Noodles',
      unit: 'Pack of 4 (240g)',
      mrp: 52,
      price: 48,
      image: createProductSVG('#fed7aa', '🍝', 'Yippee Noodles'),
      rack: 'Aisle 4 • Shelf B1',
      tags: ['yippee', 'noodles', 'instant'],
      stock: 45
    },
    {
      id: 'p-504',
      categoryId: 'cat-instant',
      title: 'MTR Ready-to-Eat Paneer Butter Masala',
      unit: '300 g',
      mrp: 140,
      price: 125,
      image: createProductSVG('#fecaca', '🍛', 'Paneer Curry'),
      rack: 'Aisle 4 • Shelf B2',
      tags: ['mtr', 'ready to eat', 'paneer'],
      stock: 20
    },
    {
      id: 'p-505',
      categoryId: 'cat-instant',
      title: 'Quaker Oats (Whole Grain)',
      unit: '1 kg Pouch',
      mrp: 199,
      price: 175,
      image: createProductSVG('#fef08a', '🥣', 'Quaker Oats'),
      rack: 'Aisle 4 • Shelf C1',
      tags: ['oats', 'quaker', 'breakfast'],
      stock: 35
    },
    {
      id: 'p-506',
      categoryId: 'cat-instant',
      title: 'Kellogg’s Corn Flakes (Original)',
      unit: '475 g',
      mrp: 220,
      price: 195,
      image: createProductSVG('#fef08a', '🥣', 'Corn Flakes'),
      rack: 'Aisle 4 • Shelf C2',
      tags: ['cornflakes', 'kelloggs', 'cereal'],
      stock: 30
    },
    {
      id: 'p-507',
      categoryId: 'cat-instant',
      title: 'Top Ramen Curry Noodles',
      unit: '280 g (4 Packs)',
      mrp: 60,
      price: 55,
      image: createProductSVG('#fed7aa', '🍜', 'Top Ramen'),
      rack: 'Aisle 4 • Shelf D1',
      tags: ['top ramen', 'curry', 'noodles'],
      stock: 40
    },
    {
      id: 'p-508',
      categoryId: 'cat-instant',
      title: 'Chings Secret Schezwan Noodles',
      unit: '240 g',
      mrp: 55,
      price: 50,
      image: createProductSVG('#fca5a5', '🌶️', 'Chings Noodles'),
      rack: 'Aisle 4 • Shelf D2',
      tags: ['chings', 'schezwan', 'spicy'],
      stock: 35
    },

    // --- 6. Cleaning & Household (8 Items) ---
    {
      id: 'p-601',
      categoryId: 'cat-cleaning',
      title: 'Vim Dishwash Liquid Gel',
      unit: '500 ml Bottle',
      mrp: 125,
      price: 109,
      image: createProductSVG('#bbf7d0', '🧼', 'Vim Gel'),
      rack: 'Aisle 5 • Shelf A1',
      tags: ['dishwash', 'vim', 'gel'],
      stock: 40
    },
    {
      id: 'p-602',
      categoryId: 'cat-cleaning',
      title: 'Surf Excel Easy Wash Powder',
      unit: '1 kg',
      mrp: 150,
      price: 135,
      image: createProductSVG('#bfdbfe', '🧺', 'Detergent'),
      rack: 'Aisle 5 • Shelf B1',
      tags: ['detergent', 'surf excel', 'laundry'],
      stock: 35
    },
    {
      id: 'p-603',
      categoryId: 'cat-cleaning',
      title: 'Harpic Disinfectant Toilet Cleaner',
      unit: '500 ml',
      mrp: 105,
      price: 95,
      image: createProductSVG('#bfdbfe', '🚽', 'Harpic Cleaner'),
      rack: 'Aisle 5 • Shelf B2',
      tags: ['harpic', 'toilet', 'cleaner'],
      stock: 45
    },
    {
      id: 'p-604',
      categoryId: 'cat-cleaning',
      title: 'Lizol Floor Cleaner (Citrus)',
      unit: '500 ml',
      mrp: 110,
      price: 99,
      image: createProductSVG('#fef08a', '🧹', 'Lizol Floor'),
      rack: 'Aisle 5 • Shelf C1',
      tags: ['lizol', 'floor', 'citrus'],
      stock: 50
    },
    {
      id: 'p-605',
      categoryId: 'cat-cleaning',
      title: 'Colin Glass & Surface Cleaner',
      unit: '500 ml Spray',
      mrp: 115,
      price: 102,
      image: createProductSVG('#93c5fd', '🪟', 'Colin Spray'),
      rack: 'Aisle 5 • Shelf C2',
      tags: ['colin', 'glass', 'cleaner'],
      stock: 25
    },
    {
      id: 'p-606',
      categoryId: 'cat-cleaning',
      title: 'Comfort After Wash Fabric Conditioner',
      unit: '860 ml',
      mrp: 235,
      price: 210,
      image: createProductSVG('#ddd6fe', '🌸', 'Comfort Softener'),
      rack: 'Aisle 5 • Shelf D1',
      tags: ['comfort', 'fabric', 'softener'],
      stock: 30
    },
    {
      id: 'p-607',
      categoryId: 'cat-cleaning',
      title: 'Godrej Aer Pocket Bathroom Fragrance',
      unit: '10 g (Violet Valley)',
      mrp: 60,
      price: 55,
      image: createProductSVG('#e9d5ff', '🌺', 'Godrej Aer'),
      rack: 'Aisle 5 • Shelf D2',
      tags: ['godrej', 'aer', 'air freshener'],
      stock: 60
    },
    {
      id: 'p-608',
      categoryId: 'cat-cleaning',
      title: 'Origami 2-Ply Facial Tissues',
      unit: 'Box of 100 Pulls',
      mrp: 85,
      price: 75,
      image: createProductSVG('#ffffff', '🧻', 'Tissue Box'),
      rack: 'Aisle 5 • Shelf E1',
      tags: ['tissue', 'origami', 'paper'],
      stock: 40
    },

    // --- 7. Personal Care (8 Items) ---
    {
      id: 'p-701',
      categoryId: 'cat-personal',
      title: 'Dettol Original Liquid Handwash',
      unit: '200 ml Refill',
      mrp: 99,
      price: 89,
      image: createProductSVG('#dcfce7', '🧴', 'Dettol Handwash'),
      rack: 'Aisle 6 • Shelf A1',
      tags: ['handwash', 'dettol', 'hygiene'],
      stock: 50
    },
    {
      id: 'p-702',
      categoryId: 'cat-personal',
      title: 'Colgate Strong Teeth Toothpaste',
      unit: '150 g',
      mrp: 110,
      price: 98,
      image: createProductSVG('#fca5a5', '🪥', 'Toothpaste'),
      rack: 'Aisle 6 • Shelf B1',
      tags: ['toothpaste', 'colgate', 'dental'],
      stock: 60
    },
    {
      id: 'p-703',
      categoryId: 'cat-personal',
      title: 'Dove Cream Beauty Bathing Soap',
      unit: '75 g (Pack of 3)',
      mrp: 165,
      price: 145,
      image: createProductSVG('#ffffff', '🧼', 'Dove Soap'),
      rack: 'Aisle 6 • Shelf B2',
      tags: ['dove', 'soap', 'bathing'],
      stock: 45
    },
    {
      id: 'p-704',
      categoryId: 'cat-personal',
      title: 'Head & Shoulders Anti-Dandruff Shampoo',
      unit: '180 ml',
      mrp: 190,
      price: 169,
      image: createProductSVG('#93c5fd', '🧴', 'H&S Shampoo'),
      rack: 'Aisle 6 • Shelf C1',
      tags: ['shampoo', 'head and shoulders', 'hair'],
      stock: 35
    },
    {
      id: 'p-705',
      categoryId: 'cat-personal',
      title: 'Nivea Soft Light Moisturiser Cream',
      unit: '100 ml Tub',
      mrp: 210,
      price: 185,
      image: createProductSVG('#e0f2fe', '🧴', 'Nivea Soft'),
      rack: 'Aisle 6 • Shelf C2',
      tags: ['nivea', 'cream', 'skin'],
      stock: 30
    },
    {
      id: 'p-706',
      categoryId: 'cat-personal',
      title: 'Gillette Mach3 Turbo Razor',
      unit: '1 Razor Handle + 1 Cartridge',
      mrp: 325,
      price: 289,
      image: createProductSVG('#bfdbfe', '🪒', 'Gillette Razor'),
      rack: 'Aisle 6 • Shelf D1',
      tags: ['gillette', 'razor', 'shaving'],
      stock: 20
    },
    {
      id: 'p-707',
      categoryId: 'cat-personal',
      title: 'Stayfree Secure Extra Large Pads',
      unit: '20 Wings Pads',
      mrp: 180,
      price: 159,
      image: createProductSVG('#fbcfe8', '🌸', 'Stayfree Pads'),
      rack: 'Aisle 6 • Shelf D2',
      tags: ['stayfree', 'pads', 'sanitary'],
      stock: 40
    },
    {
      id: 'p-708',
      categoryId: 'cat-personal',
      title: 'Pampers Baby Dry Diapers (Medium)',
      unit: 'Pack of 20 Diapers',
      mrp: 399,
      price: 349,
      image: createProductSVG('#fef08a', '👶', 'Pampers Medium'),
      rack: 'Aisle 6 • Shelf E1',
      tags: ['pampers', 'diapers', 'baby care'],
      stock: 25
    }
  ]
};
