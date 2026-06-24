// admin.js - Admin product management logic

document.addEventListener('DOMContentLoaded', () => {
    // Check if user is authenticated and role is admin
    const user = window.auth.checkAuth();
    if (!user || user.role !== 'admin') {
        if (user) {
             window.location.href = 'index.html'; 
        }
        return;
    }

    const tableContainer = document.getElementById('products-table-container');
    const modal = document.getElementById('product-modal');
    const form = document.getElementById('product-form');
    const addBtn = document.getElementById('add-product-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const modalTitle = document.getElementById('modal-title');

    // Load products on start
    loadProducts();

    // Event Listeners
    addBtn.addEventListener('click', () => openModal());
    cancelBtn.addEventListener('click', closeModal);
    form.addEventListener('submit', handleSave);

    // Global click listener for edit/delete buttons inside the table
    tableContainer.addEventListener('click', async (e) => {
        if (e.target.classList.contains('edit-btn')) {
            const id = e.target.getAttribute('data-id');
            await openModalForEdit(id);
        } else if (e.target.classList.contains('delete-btn')) {
            const id = e.target.getAttribute('data-id');
            if (confirm('Are you sure you want to delete this product?')) {
                await deleteProduct(id);
            }
        }
    });

    async function loadProducts() {
        try {
            const products = await window.api.fetch('/products', { method: 'GET' });
            renderTable(products);
        } catch (error) {
            tableContainer.innerHTML = '';
            window.api.showError('admin-error', 'Failed to load products: ' + error.message);
        }
    }

    function renderTable(products) {
        if (!products || products.length === 0) {
            tableContainer.innerHTML = '<p style="padding: 2rem; text-align: center; color: var(--text-muted);">No products found.</p>';
            return;
        }

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Category</th>
                        <th>Color</th>
                        <th>Size</th>
                        <th>Price</th>
                        <th>Stock</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
        `;

        products.forEach(p => {
            html += `
                <tr>
                    <td>${p.id}</td>
                    <td>${p.name}</td>
                    <td>${p.category}</td>
                    <td>${p.color}</td>
                    <td>${p.size}</td>
                    <td style="color: #34d399; font-weight: 500;">$${p.price}</td>
                    <td>${p.stock || p.quantity}</td>
                    <td>
                        <button class="btn edit-btn" data-id="${p.id}" style="padding: 0.25rem 0.75rem; font-size: 0.8rem; background: var(--primary); width: auto;">Edit</button>
                        <button class="btn delete-btn" data-id="${p.id}" style="padding: 0.25rem 0.75rem; font-size: 0.8rem; background: var(--danger); width: auto; margin-left: 0.5rem;">Delete</button>
                    </td>
                </tr>
            `;
        });

        html += '</tbody></table>';
        tableContainer.innerHTML = html;
    }

    function openModal(product = null) {
        if (product) {
            modalTitle.innerText = 'Edit Product';
            document.getElementById('product-id').value = product.id;
            document.getElementById('product-name').value = product.name;
            document.getElementById('product-category').value = product.category;
            document.getElementById('product-color').value = product.color;
            document.getElementById('product-size').value = product.size;
            document.getElementById('product-price').value = product.price;
            document.getElementById('product-stock').value = product.stock || product.quantity;
        } else {
            modalTitle.innerText = 'Add Product';
            form.reset();
            document.getElementById('product-id').value = '';
        }
        modal.classList.add('active');
    }

    function closeModal() {
        modal.classList.remove('active');
        form.reset();
    }

    async function openModalForEdit(id) {
        // Ideally we fetch a single product, or find it in the current list.
        // Fast approach: fetch the list and find it.
        try {
            const products = await window.api.fetch('/products', { method: 'GET' });
            const product = products.find(p => p.id == id);
            if (product) {
                openModal(product);
            }
        } catch (error) {
            alert('Failed to fetch product details.');
        }
    }

    async function handleSave(e) {
        e.preventDefault();
        
        const id = document.getElementById('product-id').value;
        const payload = {
            name: document.getElementById('product-name').value,
            category: document.getElementById('product-category').value,
            color: document.getElementById('product-color').value,
            size: document.getElementById('product-size').value,
            price: parseFloat(document.getElementById('product-price').value),
            stock: parseInt(document.getElementById('product-stock').value, 10),
        };

        const isEdit = !!id;
        const endpoint = isEdit ? `/products/${id}` : '/products';
        const method = isEdit ? 'PUT' : 'POST';

        try {
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerText = 'Saving...';

            await window.api.fetch(endpoint, {
                method: method,
                body: JSON.stringify(payload)
            });

            closeModal();
            loadProducts(); // Refresh list

        } catch (error) {
            alert('Failed to save product: ' + error.message);
        } finally {
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.innerText = 'Save';
        }
    }

    async function deleteProduct(id) {
        try {
            await window.api.fetch(`/products/${id}`, { method: 'DELETE' });
            loadProducts(); // Refresh list
        } catch (error) {
            alert('Failed to delete product: ' + error.message);
        }
    }
});
