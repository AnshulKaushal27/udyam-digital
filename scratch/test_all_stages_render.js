const fs = require('fs');
const vm = require('vm');

const jsCode = fs.readFileSync('scratch/consumer_extracted.js', 'utf8');

// Create mock DOM elements
class MockElement {
  constructor(id = '') {
    this.id = id;
    this.innerText = '';
    this.innerHTML = '';
    this.value = '';
    this.className = '';
    this.classList = {
      add: (c) => {},
      remove: (c) => {},
      contains: (c) => false
    };
    this.style = {};
    this.children = [];
  }
  appendChild(child) {
    this.children.push(child);
  }
  addEventListener(evt, fn) {}
  focus() {}
}

const elements = {};
function getOrCreateElement(id) {
  if (!elements[id]) {
    elements[id] = new MockElement(id);
  }
  return elements[id];
}

const sandbox = {
  window: {
    addEventListener: () => {},
    AudioContext: function() {
      this.state = 'running';
      this.resume = () => {};
      this.createOscillator = () => ({ frequency: { setValueAtTime: () => {} }, connect: () => {}, start: () => {}, stop: () => {} });
      this.createGain = () => ({ gain: { setValueAtTime: () => {}, linearRampToValueAtTime: () => {}, exponentialRampToValueAtTime: () => {} }, connect: () => {} });
      this.destination = {};
      this.currentTime = 0;
    }
  },
  document: {
    getElementById: (id) => getOrCreateElement(id),
    createElement: (tag) => new MockElement(tag),
    querySelector: (sel) => new MockElement(sel),
    querySelectorAll: (sel) => [],
    addEventListener: () => {}
  },
  localStorage: {
    getItem: () => null,
    setItem: () => {}
  },
  console: console,
  setTimeout: setTimeout,
  clearTimeout: clearTimeout,
  fetch: () => Promise.resolve({ json: () => Promise.resolve({}) })
};

sandbox.window.document = sandbox.document;
sandbox.global = sandbox;

try {
  vm.createContext(sandbox);
  vm.runInContext(jsCode, sandbox);
  console.log("Script evaluated successfully without top-level errors.");
} catch (err) {
  console.error("Top-level evaluation error:", err);
  process.exit(1);
}

// Now let's test calling renderWorkspaceContent() across ALL stages!
const testWorkflows = [
  {
    stage: "USER_TYPE_SELECTION",
    user_type: null,
    discovery: { requirements: [], business_type: "kirana" },
    recommendation: { active_addons: [], line_items: [] },
    customer: {},
    messages: []
  },
  {
    stage: "CUSTOMER_ACCOUNT_CHECK",
    user_type: "customer",
    discovery: { requirements: [], business_type: "kirana" },
    recommendation: { active_addons: [], line_items: [] },
    customer: {},
    messages: []
  },
  {
    stage: "BUSINESS_IDENTIFICATION",
    user_type: "customer",
    discovery: { requirements: [], business_type: "kirana" },
    recommendation: { active_addons: [], line_items: [] },
    customer: {},
    messages: []
  },
  {
    stage: "REQUIREMENTS_COLLECTION",
    user_type: "customer",
    discovery: { requirements: ["broadband_speed", "cctv_security"], business_type: "kirana" },
    recommendation: { active_addons: ["P01", "P23"], line_items: [] },
    customer: {},
    messages: []
  },
  {
    stage: "PLAN_EXPLORATION",
    user_type: "customer",
    discovery: { requirements: ["broadband_speed", "cctv_security"], business_type: "kirana" },
    recommendation: {
      bundle_id: "bundle_kirana",
      bundle_name: "Kirana Digital Starter",
      monthly_base: 1999,
      monthly_subtotal: 2799,
      gst_18: 504,
      total_monthly: 3303,
      setup_fee: 2200,
      contract_months: 12,
      active_addons: ["P23"],
      included_products: [{ id: "P04", name: "Biz 5G AirFiber" }, { id: "P09", name: "Backup Failover" }],
      line_items: [
        { product_id: "P04", name: "Base Plan: Kirana Digital Starter", quantity: 1, monthly_before_tax: 1999, setup_fee: 1000, contract_months: 12, type: "base_plan" },
        { product_id: "P23", name: "24/7 Cloud CCTV", quantity: 1, monthly_before_tax: 800, setup_fee: 1200, contract_months: 12, type: "addon" },
        { product_id: "P09", name: "Included: 4G Failover", quantity: 1, monthly_before_tax: 0, setup_fee: 0, contract_months: 12, type: "included_component", is_included: true }
      ]
    },
    customer: { name: "anni", business_name: "vadvava", authenticated: true },
    messages: [
      { sender: "bot", text: "Based on your business needs...", quick_replies: ["Confirm Quote & Start KYC", "Customize Add-ons"] }
    ]
  },
  {
    stage: "PLAN_EXPLORATION",
    user_type: "customer",
    discovery: {},
    recommendation: {},
    customer: {},
    messages: []
  },
  {
    stage: "PLAN_EXPLORATION",
    user_type: "customer",
    discovery: null,
    recommendation: null,
    customer: null,
    messages: []
  },
  {
    stage: "KYC_VERIFICATION",
    user_type: "customer",
    discovery: { requirements: [], business_type: "kirana" },
    recommendation: { bundle_name: "Kirana Digital Starter", total_monthly: 2359, line_items: [] },
    customer: { name: "anni", business_name: "vadvava", authenticated: true },
    kyc: { status: "PENDING", documents: [] },
    messages: []
  },
  {
    stage: "INSTALLATION_TRACKING",
    user_type: "customer",
    discovery: { requirements: [], business_type: "kirana" },
    recommendation: { bundle_name: "Kirana Digital Starter", total_monthly: 2359 },
    customer: { name: "anni", business_name: "vadvava", authenticated: true },
    order: { order_id: "ORD-1234", milestone: 3, milestone_text: "Dispatched", engineer_name: "Rahul", engineer_phone: "9810123456" },
    messages: []
  }
];

let failed = false;
for (const wf of testWorkflows) {
  try {
    vm.runInContext("activeWorkflow = " + JSON.stringify(wf) + "; renderContextualWorkspace(); renderChatThread();", sandbox);
    console.log(`[PASS] Rendered stage: ${wf.stage}`);
  } catch (err) {
    console.error(`[FAIL] Error rendering stage ${wf.stage}:`, err.message);
    failed = true;
  }
}

if (failed) {
  process.exit(1);
} else {
  console.log("All stage rendering tests passed!");
}
